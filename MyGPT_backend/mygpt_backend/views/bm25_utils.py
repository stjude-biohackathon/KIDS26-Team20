#libraries to import for keyword search
import bm25s
import Stemmer
from tqdm import tqdm
import numpy as np
import shutil
# from nltk.stem.snowball import SnowballStemmer
from .rerank_utils import (
    rerank_sources
)
from .helpers import safe_path, validate_dataset_name

#this method should be called as part of the upload document process just after adding chunks into the chromadb
def index_document_by_bm25(dataset_name, language_of_docs='english', progress_callback=None):
    dataset_name = validate_dataset_name(dataset_name)
    tokenizer_directory = safe_path('/code/data/bm25_tokenizer', dataset_name)
    tokenizer_directory.mkdir(parents=True, exist_ok=True)
    documents_file = safe_path('/code/data/data_chunks', dataset_name + '.txt')

    documents = []

    # First, count total lines for progress tracking
    total_lines = 0
    with documents_file.open('r') as file:
        total_lines = sum(1 for _ in file)

    with documents_file.open('r') as file:
        for line_number, line in enumerate(
                tqdm((file.readlines()), desc=f'Reading {dataset_name}'), 100
        ):
            # Strip whitespace and append the line to the documents list
            line = line.strip()
            # convert line to json
            line_json = eval(line)
            documents.append('document ' + str(line_json['title']) +  '; page ' + str(line_json['page'])+ '; ' + line_json['content'].strip())
            
            # Report progress for reading phase
            if progress_callback and total_lines > 0:
                progress = 25 + int((line_number / total_lines) * 10)
                progress_callback('bm25_indexing', min(progress, 35), f'Reading documents: {line_number}/{total_lines}')

    if progress_callback:
        progress_callback('bm25_indexing', 40, 'Building BM25 index...')

    # default tokenizer
    stemmer = Stemmer.Stemmer(language_of_docs.lower())
    tokenizer = bm25s.tokenization.Tokenizer(stemmer=stemmer)
    corpus_tokenized = tokenizer.tokenize(documents, return_as='tuple')

    if progress_callback:
        progress_callback('bm25_indexing', 45, 'Indexing documents...')

    retriever = bm25s.BM25(corpus=documents)
    retriever.index(corpus_tokenized)
    
    if progress_callback:
        progress_callback('bm25_indexing', 48, 'Saving BM25 index...')
    
    retriever.save(tokenizer_directory)
    tokenizer.save_vocab(tokenizer_directory)
    tokenizer.save_stopwords(tokenizer_directory)

def retrieve_chunks_by_bm25(queryText, dataset_name, focused_document_titles=[], chunk_count=10, reranker='None', language_of_docs='english'):
    dataset_name = validate_dataset_name(dataset_name)
    chunk_file = safe_path('/code/data/data_chunks', dataset_name + '.txt')
    tokenizer_directory = safe_path('/code/data/bm25_tokenizer', dataset_name)

    stemmer = Stemmer.Stemmer(language_of_docs.lower())
    # french_stemmer = SnowballStemmer("french")

     # Tokenize the queries
    queriesTokenized = bm25s.tokenize([queryText], stemmer=stemmer)
    # queriesTokenized = bm25s.tokenize([queryText], stemmer=french_stemmer)

    results = []
    scores = []
    # if focused_document_titles is not empty, get the chunk file and create weight mask for the documents
    if focused_document_titles != []:
        with chunk_file.open('r') as file:
            chunk_lines = file.readlines()
        for document_title in focused_document_titles:
            weight_mask = np.array([1 if "'title': '" + str(document_title) + "'" in line else 0 for line in chunk_lines])

            retriever_loaded = bm25s.BM25.load(tokenizer_directory, mmap=True, load_corpus=True)
            results_temp, scores_temp = retriever_loaded.retrieve(queriesTokenized, k=chunk_count, return_as="tuple", weight_mask=weight_mask if document_title != '' else None)
            results.extend(results_temp)
            scores.extend(scores_temp)
    else:
        retriever_loaded = bm25s.BM25.load(tokenizer_directory, mmap=True, load_corpus=True)
        results, scores = retriever_loaded.retrieve(queriesTokenized, k=chunk_count, return_as="tuple")

    if reranker != 'None':
        # rerank the sources based on cross encoder
        prererank_results = []
        reranked_results = []
        prereranked_bm25_scores = []
        for idx, result in enumerate(results[0]):
            prereranked_bm25_scores.append(scores[0][idx])
            prererank_results.append({
                'context': result['text'],
                'bm25_score_raw': scores[0][idx],
            })
        reranked_results = rerank_sources(prererank_results, queryText, reranker, language_of_docs)
        results_ = []
        for reranked_result in reranked_results:
            results_.append({
                'text': reranked_result['context'],
                'reranked_score': reranked_result['reranked_score'],
            })
        results = [results_]
        scores = [[i['bm25_score_raw'] for i in reranked_results]]
    # returns ids of the chunks as a list
    return results[0], scores[0]

def hybrid_source_combination(vector_sources, bm25_sources):
    # find duplicates from both the list with same text
    duplicates = []
    combined_sources = []
    if len(bm25_sources) == 0:
        # if vector sources are empty, return bm25 sources
        return vector_sources
    
    for vector_source in vector_sources:
        for bm25_source in bm25_sources:
            if vector_source['vector_score'] < 0.1 and bm25_source['bm25_score'] < 0.1:
                continue
            if vector_source['context'] == bm25_source['context'] and vector_source['page'] == bm25_source['page']:
                # create a new source with the same text and distance from bm25
                new_source = vector_source.copy()
                new_source['bm25_score_raw'] = bm25_source['bm25_score_raw']
                new_source['bm25_score'] = bm25_source['bm25_score']
                new_source['bm25_rank'] = bm25_source['rank']
                duplicates.append(new_source)
                break

    # add the vector sources to the combined sources not present in duplicates
    for vector_source in vector_sources:
        if vector_source['vector_score'] < 0.1:
            continue
        # check if the source is already in the combined sources
        for duplicate in duplicates:
            if vector_source['context'] == duplicate['context'] and vector_source['page'] == duplicate['page']:
                break
        else:
            # add the vector source to the combined sources
            combined_sources.append(vector_source)
    
    # add the duplicates to the combined sources
    combined_sources.extend(duplicates)

    # add the bm25 sources to the combined sources
    for bm25_source in bm25_sources:
        if  bm25_source['bm25_score'] < 0.1:
            continue
        # check if the source is already in the combined sources
        for duplicate in duplicates:
            if bm25_source['context'] == duplicate['context'] and bm25_source['page'] == duplicate['page']:
                break
        else:
            # add the bm25 source to the combined sources
            combined_sources.append(bm25_source)

    return combined_sources

def get_answer_distance_by_context_bm25(text, contexts = [''], language_of_docs='english'):

    tokenizer_directory = safe_path('/code/data/bm25_tokenizer', 'answers')
    tokenizer_directory.mkdir(parents=True, exist_ok=True)

    # default tokenizer
    stemmer = Stemmer.Stemmer(language_of_docs.lower())
    tokenizer = bm25s.tokenization.Tokenizer(stemmer=stemmer)
    corpus_tokenized = tokenizer.tokenize(contexts, return_as='tuple')

    retriever = bm25s.BM25(corpus=contexts)
    retriever.index(corpus_tokenized)
    retriever.save(tokenizer_directory)
    tokenizer.save_vocab(tokenizer_directory)
    tokenizer.save_stopwords(tokenizer_directory)

     # Tokenize the queries
    queriesTokenized = bm25s.tokenize([text], stemmer=stemmer)

    retriever_loaded = bm25s.BM25.load(tokenizer_directory, mmap=True, load_corpus=True)

    # Get the top 10 results
    results, scores = retriever_loaded.retrieve(queriesTokenized, k=len(contexts), return_as="tuple")

    # delete the tokenizer directory after use
    shutil.rmtree(tokenizer_directory)

    # returns ids of the chunks as a list
    return results[0], scores[0]