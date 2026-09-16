"""
Embedding model utilities and functions
"""
import os
import numpy as np
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from django.utils.timezone import make_aware
import datetime
from tqdm import tqdm

from ..models import EmbeddingModel, Question, Answer, chunks, Dataset, Papers, Videos
from .embedding_functions import HuggingFaceEmbeddingFunction, OllamaEmbeddingFunction


def get_embedding_model_ef(embedding_model_request, add_distances=False):
    """Get the embedding function for the specified model"""
    # query embedding model from database
    embedding_model_count = EmbeddingModel.objects.filter(model_name=embedding_model_request).count()
    add_embedding_model_distances = False
    if embedding_model_count == 0:
        EmbeddingModel.objects.create(
            model_name=embedding_model_request,
            model_source='sentence-transformer'
        )
        embedding_model = embedding_model_request
        embedding_model_source = 'sentence-transformer'
        add_embedding_model_distances = True
    else:
        embedding_model = EmbeddingModel.objects.filter(model_name=embedding_model_request)[0].model_name
        embedding_model_source = EmbeddingModel.objects.filter(model_name=embedding_model_request)[0].model_source
        
    # use multi-qa-MiniLM-L6-cos-v1 embedding function
    if embedding_model == 'all-MiniLM-L6-v2':
        embedding_model_ef = embedding_functions.DefaultEmbeddingFunction()
    elif embedding_model_source == 'ollama':
        embedding_model_ef = OllamaEmbeddingFunction(url=os.environ.get('OLLAMA_SERVER') + "/api/embeddings", model_name=embedding_model.split(':')[0]) 
    elif '/' in embedding_model:
        embedding_model_ef = HuggingFaceEmbeddingFunction(api_key=os.environ.get('HUGGINGFACE_API_KEY'), model_name=embedding_model)
    elif embedding_model_source == 'sentence-transformer':    
        embedding_model_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model)

    if add_embedding_model_distances or add_distances:
        # read csv file from ./data/cutoff_examples/cutoff_data.csv
        df = pd.read_csv('/code/data/cutoff_examples/cutoff_data.csv')
        embedding_model = EmbeddingModel.objects.filter(model_name=embedding_model_request)[0]
        for i in range(len(df)):
            if df['distance_tag'][i] == 'best_q':
                question = df['question'][i]
                answer = df['answer'][i]
                answer_no_context = df['answer_without_context'][i]
                chunks = df['context_chunks'][i].split(';')
                distances_q, distances_a, distance_na = get_embedding_cutoff_distance(embedding_model_ef, chunks, question, answer, answer_no_context)
                embedding_model.best_distance_q = np.round(distances_q, 3)
                embedding_model.best_distance_ac = np.round(distances_a, 3)
                embedding_model.worst_distance_nac = np.round(distance_na, 3)
            elif df['distance_tag'][i] == 'worst_q':
                question = df['question'][i]
                answer = df['answer'][i]
                answer_no_context = df['answer_without_context'][i]
                chunks = df['context_chunks'][i].split(';')
                distances_q, distances_a, _ = get_embedding_cutoff_distance(embedding_model_ef, chunks, question, answer, answer_no_context)
                embedding_model.worst_distance_q = np.round(distances_a, 3)
            elif df['distance_tag'][i] == 'worst_a':
                question = df['question'][i]
                answer = df['answer'][i]
                answer_no_context = df['answer_without_context'][i]
                chunks = df['context_chunks'][i].split(';')
                _, distances_a, distance_na = get_embedding_cutoff_distance(embedding_model_ef, chunks, question, answer, answer_no_context)
                embedding_model.worst_distance_ac = np.round(distances_a, 3)
                embedding_model.best_distance_nac = np.round(distance_na, 3)
        embedding_model.save()
                        
    return embedding_model_ef


def get_embedding_cutoff_distance(embedding_model_ef, chunks, question, answer, answer_no_context):
    """Calculate cutoff distances for question, answer with context, and answer without context"""
    # create a collection
    client = chromadb.PersistentClient(path='/code/chroma_storage/.')
    dataset_name = 'mygpt_distance_dataset'
    if len(client.list_collections()):
        for collection in client.list_collections():
            if collection.name == dataset_name:
                client.delete_collection(name=dataset_name)

    collection = client.create_collection(name=dataset_name, embedding_function=embedding_model_ef)

    # add chunks to collection
    ids = [str(i) for i in range(len(chunks))]
    collection.add(
        ids=ids,
        documents=chunks
    )

    # get distances between question and chunks
    results = collection.query(
        query_texts=[question],
        n_results=len(chunks)
    )

    distances_q = results['distances'][0]
    distance_q = distances_q[0]

    # get distances between answer and chunks
    results = collection.query(
        query_texts=[answer],
        n_results=len(chunks)
    )

    distances_a = results['distances'][0]
    distance_a = distances_a[0]

    # get distances between answer_no_context and chunks
    results = collection.query(
        query_texts=[answer_no_context],
        n_results=len(chunks)
    )

    distances_na = results['distances'][0]
    distance_na = sum(distances_na) / len(distances_na)

    # empty collection
    collection.delete(ids=ids)
    client.delete_collection(name=dataset_name)

    return distance_q, distance_a, distance_na


def add_embeddings_to_chunks(dataset):
    """Add embeddings to chunks in the database"""
    # get chunks by reading text file
    chunks_txt = []
    with open('data/data_chunks/'+ str(dataset) +'.txt', 'r') as file:
        for line in file:
            chunk = eval(line)
            chunks_txt.append(chunk)

    # find papers or videos
    dataset_obj = Dataset.objects.get(dataset_name=dataset)
    library_type = ''
    papers = Papers.objects.filter(paper_dataset=dataset_obj)
    videos = Videos.objects.filter(video_dataset=dataset_obj)
    if papers.count() > 0:
        library_type = 'papers'
    elif videos.count() > 0:
        library_type = 'videos'
    
    for i in tqdm(
        range(0, len(chunks_txt), 100), desc='Adding embeddings', unit_scale=100
    ):
        default_ef = OllamaEmbeddingFunction(url=os.environ.get('OLLAMA_SERVER') + "/api/embeddings", model_name='nomic-embed-text')
        for chunk in chunks_txt[i : i + 100]:
            embedding = default_ef([chunk['content']])
            chunk = chunks.objects.create(
                chunk_text=chunk['content'],
                embedding=embedding,
                chunk_dataset=dataset_obj,
                chunk_paper= Papers.objects.filter(paper_title=chunk['title'])[0] if library_type == 'papers' else None,
                chunk_video= Videos.objects.filter(video_title=chunk['title'])[0] if library_type == 'videos' else None,
                chunk_date_time=make_aware(datetime.datetime.now())
            )
    
    #  update dataset
    dataset = Dataset.objects.get(dataset_name=dataset)
    dataset.embedding_added = True
    dataset.save()

    return


def add_embeddings_to_qna(text, text_type='question', embedding_model_request='multi-qa-MiniLM-L6-cos-v1'):
    """Add embeddings to questions or answers"""
    embedding_model_ef = get_embedding_model_ef(embedding_model_request)

    # get embeddings
    embedding = embedding_model_ef([text])

    if text_type == 'question':
        question_obj = Question.objects.filter(question_text=text)
        if question_obj.count() > 0:
            question = question_obj[0]
            question.embedding = embedding
            question.save()
        else:
            question = Question.objects.create(
                question_text=text,
                embedding=embedding,
                saved_date_time=make_aware(datetime.datetime.now())
            )
    elif text_type == 'answer':
        answer_obj = Answer.objects.filter(answer_text=text)
        if answer_obj.count() > 0:
            answer = answer_obj[0]
            answer.embedding = embedding
            answer.save()
        else:
            answer = Answer.objects.create(
                answer_text=text,
                embedding=embedding,
                saved_date_time=make_aware(datetime.datetime.now())
            )

    return
