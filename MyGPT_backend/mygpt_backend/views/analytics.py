"""
Analytics and scoring functions (PCA, relevance scoring)
"""
import numpy as np
import pandas as pd
from tqdm import tqdm

from ..models import chunks, Question, Answer, Source, EmbeddingModel
from .helpers import min_max_normalization


def add_pca_to_chunks():
    """Add PCA embeddings to chunks"""
    chunks_objects = chunks.objects.all()
    embddings = []
    for chunk in chunks_objects:
        embddings.append(eval(chunk.embedding)[0])

    # perform pca on embeddings with numpy
    data = pd.DataFrame(embddings)
    data = data - data.mean()

    # calculate covariance matrix
    cov_matrix = data.cov()

    # calculate eigen values and eigen vectors
    eigen_values, eigen_vectors = np.linalg.eig(cov_matrix)

    # sort eigen values and eigen vectors
    idx = eigen_values.argsort()[::-1]
    eigen_values = eigen_values[idx]
    eigen_vectors = eigen_vectors[:,idx]

    # select top 3 eigen vectors
    pca = eigen_vectors[:, :3]

    # project data to 2D
    embeddings_pca = data.dot(pca)

    # write pca embeddings to file
    # remove imaginary part
    embeddings_pca_short = np.real(embeddings_pca)
    # convert to 2 decimal places
    embeddings_pca_short = np.round(embeddings_pca_short, 4)

    for idx, embedding in enumerate(embeddings_pca_short):
        chunk = chunks_objects[idx]
        chunk.pca_x = embedding[0]
        chunk.pca_y = embedding[1]
        chunk.pca_z = embedding[2]
        chunk.save()


def add_pca_to_qna_and_dataset(question_id):
    """Add PCA embeddings to question, answer, and dataset"""
    question = Question.objects.get(id=question_id)
    question_embedding = eval(question.embedding)[0]
    answer = Answer.objects.filter(question=question)[0]
    answer_embedding = eval(answer.embedding)[0]
    sources = Source.objects.filter(question=question)
    source_embeddings = []
    for source in sources:
        chunk = chunks.objects.get(id=source.chunk.id)
        source_embedding = eval(chunk.embedding)[0]
        source_embeddings.append(source_embedding)
    chunks_objects = chunks.objects.all()
    dataset_embddings = []
    for chunk in chunks_objects:
       dataset_embddings.append(eval(chunk.embedding)[0])
    
    embeddings = []
    embeddings.append(question_embedding)
    embeddings.append(answer_embedding)
    embeddings.extend(source_embeddings)
    embeddings.extend(dataset_embddings)

    # perform pca on embeddings with numpy
    data = pd.DataFrame(embeddings)
    data = data - data.mean()

    # calculate covariance matrix
    cov_matrix = data.cov()

    # calculate eigen values and eigen vectors
    eigen_values, eigen_vectors = np.linalg.eig(cov_matrix)

    # sort eigen values and eigen vectors
    idx = eigen_values.argsort()[::-1]
    eigen_values = eigen_values[idx]
    eigen_vectors = eigen_vectors[:,idx]

    # select top 3 eigen vectors
    pca = eigen_vectors[:, :3]

    # project data to 2D
    embeddings_pca = data.dot(pca)

    # write pca embeddings to file
    # remove imaginary part
    embeddings_pca_short = np.real(embeddings_pca)
    # convert to 2 decimal places
    embeddings_pca_short = np.round(embeddings_pca_short, 4)

    question.pca_x = embeddings_pca_short[0][0]
    question.pca_y = embeddings_pca_short[0][1]
    question.pca_z = embeddings_pca_short[0][2]
    question.save()

    answer.pca_x = embeddings_pca_short[1][0]
    answer.pca_y = embeddings_pca_short[1][1]
    answer.pca_z = embeddings_pca_short[1][2]
    answer.save()

    for idx, source in enumerate(sources):
        chunk = chunks.objects.get(id=source.chunk.id)
        chunk.pca_x = embeddings_pca_short[idx+2][0]
        chunk.pca_y = embeddings_pca_short[idx+2][1]
        chunk.pca_z = embeddings_pca_short[idx+2][2]
        chunk.save()

    for idx, chunk in enumerate(chunks_objects):
        chunk.pca_x = embeddings_pca_short[idx+2+len(sources)][0]
        chunk.pca_y = embeddings_pca_short[idx+2+len(sources)][1]
        chunk.pca_z = embeddings_pca_short[idx+2+len(sources)][2]
        chunk.save()

    return


def save_chunks_pca_to_file():
    """Save chunk PCA embeddings to file"""
    chunks_objects = chunks.objects.all()
    with open('data/data_chunks/all_pca_2.txt', 'w') as file:
        for chunk in chunks_objects:
            # convert embedding into comma separated string
            embedding_str = ','.join([str(chunk.pca_x), str(chunk.pca_y), str(chunk.pca_z), chunk.chunk_dataset.dataset_name])
            file.write(embedding_str +  '\n')


def get_relevance_score(distances, embedding_model, question=True, use_default=True, qrs_lower=0, qrs_upper=1):
    """Calculate relevance score based on distances"""
    if use_default:
        embedding_model_obj = EmbeddingModel.objects.filter(model_name=embedding_model)[0]
        if question:
            best_distance = embedding_model_obj.best_distance_q
            worst_distance = embedding_model_obj.worst_distance_q
        else:
            best_distance = embedding_model_obj.best_distance_ac
            worst_distance = embedding_model_obj.worst_distance_ac

        buffer_distance = (worst_distance - best_distance) * 0.1
        best_distance = best_distance - buffer_distance
        worst_distance = worst_distance + (buffer_distance*3)
    else:
        best_distance = qrs_lower
        worst_distance = qrs_upper

    if len(distances) == 0:
        return 0, []

    # calculate confidence score
    if min(distances) > worst_distance:
        relevance_score = 0
    else:
        mean_distance = sum(distances) / len(distances)
        relevance_score = (1 - (mean_distance - best_distance) / (worst_distance - best_distance)) * 100
        # trim confidence score to 2 decimal places
        relevance_score = round(relevance_score, 0)
    normalized_distances = min_max_normalization(distances, best_distance, worst_distance, True)

    return relevance_score, normalized_distances
