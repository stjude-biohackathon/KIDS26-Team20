"""
ChromaDB vector database operations
"""
import os
import re
import json
import chromadb
import pandas as pd
import duckdb
from tqdm import tqdm
from langchain_community.llms import Ollama

from ..models import EmbeddingModel, Dataset
from .helpers import find_cutoff_distance
from .embedding_utils import get_embedding_model_ef

from .rerank_utils import (
    rerank_sources
)


# Initialize duckdb connection
con = duckdb.connect()


def add_to_chroma(dataset_name, embedding_model_request='all-MiniLM-L6-v2', distance_function='l2', chunking_method='fixed_chunk_size', reranker='None', progress_callback=None):
    """Add dataset to ChromaDB vector database"""
    documents_directory = '/code/data/data_chunks'
    documents = []
    metadatas = []
    files = [dataset_name + '.txt']

    def emit_progress(progress, message):
        if progress_callback:
            progress_callback('chroma_indexing', progress, message)

    emit_progress(52, 'Initializing ChromaDB...')

    # Instantiate a persistent chroma client in the persist_directory.
    client = chromadb.PersistentClient(path='/code/chroma_storage/.')

    embedding_model_ef = get_embedding_model_ef(embedding_model_request)
    embedding_model = EmbeddingModel.objects.filter(model_name=embedding_model_request)[0].model_name
        
    # If the collection already exists, we will delete it and create a new one.
    client.get_or_create_collection(name=dataset_name)
    client.delete_collection(name=dataset_name)
    if (distance_function == 'cosine'):
        collection = client.get_or_create_collection(name=dataset_name, embedding_function=embedding_model_ef, metadata={"hnsw:space": "cosine"})
    elif (distance_function == 'ip'):
        collection = client.get_or_create_collection(name=dataset_name, embedding_function=embedding_model_ef, metadata={"hnsw:space": "ip"})
    else:
        collection = client.get_or_create_collection(name=dataset_name, embedding_function=embedding_model_ef)

    # Create ids from the current count
    count = collection.count()
    print(f'Collection already contains {count} documents')

    # Load the documents in batches of 100
    if count == 0:
        # First pass: count total lines for progress
        total_lines = 0
        for filename in files:
            # Validate file path within safe directory
            safe_data_root = os.path.realpath(documents_directory)
            if not safe_data_root.endswith(os.sep):
                safe_data_root += os.sep

            normalized_file_path = os.path.realpath(f'{documents_directory}/{filename}')
            if not normalized_file_path.startswith(safe_data_root):
                raise ValueError(f"File path is outside the safe directory: {filename}")

            with open(normalized_file_path, 'r') as file:
                total_lines += sum(1 for _ in file)

        emit_progress(55, f'Reading {total_lines} documents...')

        for filename in files:
            # Validate file path within safe directory
            safe_data_root = os.path.realpath(documents_directory)
            if not safe_data_root.endswith(os.sep):
                safe_data_root += os.sep

            normalized_file_path = os.path.realpath(f'{documents_directory}/{filename}')
            if not normalized_file_path.startswith(safe_data_root):
                raise ValueError(f"File path is outside the safe directory: {filename}")

            with open(normalized_file_path, 'r') as file:
                for line_number, line in enumerate(
                    tqdm((file.readlines()), desc=f'Reading {filename}'), 1
                ):
                    # Strip whitespace and append the line to the documents list
                    line = line.strip()
                    #convert line to json
                    line_json = eval(line)
                    # remove new lines and extra spaces
                    line_json['content'] = re.sub(r'\s+', ' ', line_json['content']).strip()
                    documents.append(line_json['content'])
                    if chunking_method == 'structure_preserving':
                        metadatas.append({'filename': line_json['title'], 'page': line_json['page'], 'section': line_json['section'], 'type': line_json['type']})
                    else:
                        metadatas.append({'filename': line_json['title'], 'page': line_json['page'], 'type': line_json['type']})
                    
                    # Report progress
                    if total_lines > 0:
                        progress = 55 + int((line_number / total_lines) * 15)
                        emit_progress(min(progress, 70), f'Read {line_number}/{total_lines}')

        ids = [str(i) for i in range(count, count + len(documents))]
        
        emit_progress(70, f'Adding {len(documents)} documents to ChromaDB...')
        
        # add to vector database
        batch_size = 100
        total_batches = (len(documents) + batch_size - 1) // batch_size
        for batch_idx, i in enumerate(tqdm(
            range(0, len(documents), batch_size), desc='Adding documents', unit_scale=batch_size
        )):
            try:
                collection.add(
                    ids=ids[i : i + batch_size],
                    documents=documents[i : i + batch_size],
                    metadatas=metadatas[i : i + batch_size],  # type: ignore
                )
                
                # Report progress
                if total_batches > 0:
                    progress = 70 + int(((batch_idx + 1) / total_batches) * 28)
                    emit_progress(min(progress, 98), f'Added batch {batch_idx + 1}/{total_batches}')
                    
            except Exception as e:
                print(f'Error adding documents {i} to {i+batch_size}: {e}')
                # If there's an error, we can try adding the documents one by one to identify the problematic document
                for j in range(i, min(i + batch_size, len(documents))):
                    try:
                        collection.add(
                            ids=[ids[j]],
                            documents=[documents[j]],
                            metadatas=[metadatas[j]],  # type: ignore
                        )
                    except Exception as e:
                        print(f'Error adding document {j}: {e}')

        new_count = collection.count()
        dataset = Dataset.objects.get(dataset_name=dataset_name)
        dataset.dataset_size = new_count
        dataset.embedding_model = embedding_model
        dataset.use_reranker = False if reranker == 'None' else True
        dataset.reranker = reranker
        dataset.save()

        emit_progress(99, 'Finalizing...')

        print(f'Added {new_count - count} documents')
        
        emit_progress(100, 'ChromaDB indexing completed')
        
        return True

    emit_progress(100, 'ChromaDB indexing completed')
    return True


def nearestDataChroma(text, dataset_name, focused_document_titles=[], focused_section_str='', keywords_str='', embedding_model_request='multi-qa-MiniLM-L6-cos-v1', maximum_chunks_count=15, no_cutoff=False, reranker='None', language_of_docs='english'):
    """Query ChromaDB for nearest documents"""
    embedding_model_ef = get_embedding_model_ef(embedding_model_request)

    # If the collection already exists, we just return it.
    client = chromadb.PersistentClient(path='/code/chroma_storage/.')
    collection = client.get_collection(name=dataset_name, embedding_function=embedding_model_ef)

    # Create ids from the current count
    count = collection.count()
    print(f'Collection contains {count} documents')

    keywords = keywords_str.split(';') if keywords_str != '' else []
    focused_document_titles = focused_document_titles if focused_document_titles != [] else ['all']
    focused_section = focused_section_str if focused_section_str != '' else 'all'
    # remove keywords if it's '-'
    if '-' in keywords:
        keywords.remove('-')

    #  collect the results based on the keywords
    keyword_results = []
    if len(keywords) > 0:
        if ';' in keywords:
            keywords_filter = {'$and': [{'$contains': keyword} for keyword in keywords]}
            keyword_results = collection.query(
                query_texts=[text],
                n_results=2,
                where={'type': {"$ne": "spreadsheet_full"}},
                where_document={keywords_filter}
            )
        else:
            keyword_results = collection.query(
                query_texts=[text],
                n_results=2,
                where={'type': {"$ne": "spreadsheet_full"}},
                where_document={'$contains': keywords[0]}
            )

    if 'all' in focused_document_titles and focused_section == 'all':
        results = collection.query(
            query_texts=[text],
            n_results=maximum_chunks_count,
            where={'type': {"$ne": "spreadsheet_full"}}
        )
    elif 'all' not in focused_document_titles and focused_section == 'all':
        # make a filename filter for each of the focused document titles and combine them with $or operator
        filename_filter = ''
        if len(focused_document_titles) == 1:
            filename_filter = {'filename': {'$eq': focused_document_titles[0]}}
        else:
            filename_filter = {'$or': [{'filename': {'$eq': title}} for title in focused_document_titles]}
        results = collection.query(
            query_texts=[text],
            n_results=maximum_chunks_count,
            where={'$and':[
                {'type': {"$ne": "spreadsheet_full"}},
                filename_filter
            ]}
        )
    elif 'all' in focused_document_titles and focused_section != 'all':
        results = collection.query(
            query_texts=[text],
            n_results=maximum_chunks_count,
            where={'$and':[
                {'type': {"$ne": "spreadsheet_full"}},
                {'section': {'$eq': focused_section}}
            ]}
        )
    elif 'all' not in focused_document_titles and focused_section != 'all':
        # make a filename filter for each of the focused document titles and combine them with $or operator
        filename_filter = ''
        if len(focused_document_titles) == 1:
            filename_filter = {'filename': {'$eq': focused_document_titles[0]}}
        else:
            filename_filter = {'$or': [{'filename': {'$eq': title}} for title in focused_document_titles]}
        results = collection.query(
            query_texts=[text],
            n_results=maximum_chunks_count,
            where={'$and':[
                {'type': {"$ne": "spreadsheet_full"}},
                filename_filter,
                {'section': {'$eq': focused_section}}
            ]}
        )

    print('distances: ', results['distances'][0])
    library_type = 'papers'
    if len(results['metadatas'][0]) > 0 and "page" in results['metadatas'][0][0]:
        library_type = 'papers'
    elif len(results['metadatas'][0]) > 0 and "start" in results['metadatas'][0][0]:
        library_type = 'videos'

    reranked_scores = []

    if reranker != 'None':
        # rerank the sources based on cross encoder
        sources = []
        for i in range(len(results['ids'][0])):
            source = {
                'context': results['documents'][0][i],
                'filename': results['metadatas'][0][i]['filename'],
                'vector_score': round(1 - results['distances'][0][i], 3)
            }
            if library_type == 'papers':
                source['page'] = results['metadatas'][0][i]['page']
            elif library_type == 'videos':
                source['start'] = results['metadatas'][0][i]['start']
                source['end'] = results['metadatas'][0][i]['end']
            sources.append(source)
        
        reranked_sources = rerank_sources(sources, text, reranker, language_of_docs)
        
        # reconstruct results from reranked sources
        titles, pages, starts, stops, chunks, distances = [], [], [], [], [], []
        context = ''
        for source in reranked_sources:
            titles.append(source['filename'])
            if library_type == 'papers':
                pages.append(source['page'])
            elif library_type == 'videos':
                starts.append(source['start'])
                stops.append(source['end'])
            chunks.append(source['context'])
            reranked_scores.append(source['reranked_score'])
            distances.append(round(1 - source['vector_score'], 3))
            context += re.sub(r'\s+', ' ', source['context'])

    else:
        if no_cutoff:
            cutoff_distance = results['distances'][0][len(results['distances'][0])-1]
        else:
            cutoff_distance = find_cutoff_distance(results['distances'][0])
        print('cutoff_distance: ', cutoff_distance)
        titles, pages, starts, stops, chunks, distances = [], [], [], [], [], []
        context = ''

        # Extract results within cutoff distance
        for i in range(len(results['ids'][0])):
            if (results['distances'][0][i] <= cutoff_distance):
                titles.append(results['metadatas'][0][i]['filename'])
                if (library_type == 'papers'): 
                    pages.append(results['metadatas'][0][i]['page'])
                elif (library_type == 'videos'):
                    starts.append(results['metadatas'][0][i]['start'])
                    stops.append(results['metadatas'][0][i]['end'])
                chunks.append(results['documents'][0][i])
                distances.append(results['distances'][0][i])
                context += re.sub(r'\s+', ' ', results['documents'][0][i])
        
        if len(keywords) > 0:
            for i in range(len(keyword_results['ids'][0])):
                if (keyword_results['distances'][0][i] <= 1.5):
                    # check if chunk array already contains the chunk
                    if keyword_results['documents'][0][i] not in chunks:
                        titles.append(keyword_results['metadatas'][0][i]['filename'])
                        if (library_type == 'papers'): 
                            pages.append(keyword_results['metadatas'][0][i]['page'])
                        elif (library_type == 'videos'):
                            starts.append(keyword_results['metadatas'][0][i]['start'])
                            stops.append(keyword_results['metadatas'][0][i]['end'])
                        chunks.append(keyword_results['documents'][0][i])
                        distances.append(keyword_results['distances'][0][i])
                        context += re.sub(r'\s+', ' ', keyword_results['documents'][0][i])
    
    if len(results['metadatas'][0]) > 0 and results['metadatas'][0][0]['type'] == 'spreadsheet_chunk':
        fulltext_results = collection.query(
            query_texts=[text],
            n_results=3,
            where={"type": "spreadsheet_full"}
        )
        fulltext = fulltext_results['documents'][0][0]
        text_json = json.loads(fulltext)
        sql_df = pd.DataFrame.from_records(text_json)
        sql_df.columns = [re.sub(r"[^\w\s]", "", col_name).replace(" ", "_").lower().replace("unnamed_", "position_") for col_name in sql_df.columns.tolist()]
        final_cols = [x for x in sql_df.columns.tolist() if not x.removeprefix("position_").isnumeric()]
        numbered_cols = [x for x in sql_df.columns.tolist() if x.removeprefix("position_").isnumeric()]
        numbered_col_mention = ""
        if len(numbered_cols) > 0:
            numbered_col_mention = f", and numbered columns ranging from {numbered_cols[0]} to {numbered_cols[-1]}"
        instructions = f'Given a table with the following information, write a sql query that condenses the table to only include information useful to answering the provided query. The name of the table is sql_df. The names of the columns are as follows: {str(final_cols)}{numbered_col_mention}. Do not include any explanation, please only include the SQL code in your answer. The SQL code should result in another smaller table of only useful entries.'
        prompt = f'SYSTEM: {instructions}; QUERY: {text}; ANSWER FORMAT: {{"code": sql_code}}; ANSWER: '
        with open("sql_prompt.txt", "w") as file:
            file.write(prompt)
        ollama = Ollama(base_url="http://host.docker.internal:11434", model="llama3")
        response = ollama.invoke(prompt + '{')
        with open("generated_sql_query.txt", "w") as file:
            file.write(response)
        parsed_response = json.loads(response.replace('\n', ' '))
        new_df = con.sql(parsed_response['code']).df()
        
        final_table = str(new_df.to_json(orient='records'))
        with open("final_table.txt", "w") as file:
            file.write(final_table)
        context = f"SQL query: {response}; SQL parsing results: {final_table}"
    
    # with open("chroma_context.txt", "w") as file:
    #     file.write(context)

    ret = (titles, pages, starts, stops, chunks, distances, reranked_scores) if reranker != 'None' else (titles, pages, starts, stops, chunks, distances, [])
    return ret


def get_answer_distance(answer1, answer2, embedding_model_request='multi-qa-MiniLM-L6-cos-v1'):
    """Embed 2 answers into vector database and get distance between them"""
    dataset_name = 'answers'
    client = chromadb.PersistentClient(path='/code/chroma_storage/.')
        
    embedding_model_ef = get_embedding_model_ef(embedding_model_request)

    # If the collection already exists, we will delete it and create a new one.
    client.get_or_create_collection(name=dataset_name)
    client.delete_collection(name=dataset_name)
    collection = client.get_or_create_collection(name=dataset_name, embedding_function=embedding_model_ef)

    # add answers to collection
    answers = [answer1, answer2]
    ids = [str(i) for i in range(2)]
    collection.add(
        ids=ids,
        documents=answers
    )

    # get distance between the two answers
    results = collection.query(
        query_texts=[answer1],
        n_results=2
    )

    distance = results['distances'][0][1]
    
    # delete collection
    collection.delete(ids=ids)

    return distance


def get_answer_distance_by_context(text, dataset_name, contexts=[''], embedding_model_request='multi-qa-MiniLM-L6-cos-v1'):
    """Get distance between answer and specific contexts"""
    embedding_model_ef = get_embedding_model_ef(embedding_model_request)
    client = chromadb.PersistentClient(path='/code/chroma_storage/.')
    collection = client.get_collection(name=dataset_name, embedding_function=embedding_model_ef)

    context_count = len(contexts)

    if context_count == 0:
        return []

    if context_count == 1:
        results = collection.query(
            query_texts=[text],
            n_results=1,
            where={'type': {"$ne": "spreadsheet_full"}},
            where_document={'$contains': contexts[0]}
        )

        distances = results['distances'][0]
        return distances

    documents_filter_wrapper = { "$or": [] }
    for i in range(context_count):
        documents_filter_wrapper["$or"].append({ "$contains": contexts[i] })

    results = collection.query(
        query_texts=[text],
        n_results=context_count,
        where={'type': {"$ne": "spreadsheet_full"}},
        where_document=documents_filter_wrapper
    )

    distances = results['distances'][0]
    return distances