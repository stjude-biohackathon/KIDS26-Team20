from django.shortcuts import render
from ..models import Dataset, EmbeddingModel, RerankerModel
import pandas as pd

def home(request):
    datasets = Dataset.objects.all()

    # add embedding models from csv if not present in database
    df = pd.read_csv('/code/data/cutoff_examples/embedding_models_cutoffs.csv')
    for i in range(len(df)):
        model_name = df['model_name'][i]
        model_size = df['model_size'][i]
        model_source = df['model_source'][i]
        best_distance_q = df['best_distance_q'][i]
        worst_distance_q = df['worst_distance_q'][i]
        best_distance_ac = df['best_distance_ac'][i]
        worst_distance_ac = df['worst_distance_ac'][i]

        existing_model = EmbeddingModel.objects.filter(model_name=model_name).first()
        if not existing_model:
            new_model = EmbeddingModel(
                model_name=model_name,
                model_size=model_size,
                model_source=model_source,
                best_distance_q=best_distance_q,
                worst_distance_q=worst_distance_q,
                best_distance_ac=best_distance_ac,
                worst_distance_ac=worst_distance_ac,
                best_distance_nac=best_distance_ac,
                worst_distance_nac=worst_distance_ac
            )
            new_model.save()

    # create reranker model if not exists
    defaul_rerankers = [
        {'model_name': 'cross-encoder/qnli-electra-base', 'cutoff_score': 0.1},
        {'model_name': 'cross-encoder/nli-deberta-v3-base', 'cutoff_score': 0.0},
        {'model_name': 'zeroentropy/zerank-2', 'cutoff_score': 0.3},
        {'model_name': 'Alibaba-NLP/gte-multilingual-reranker-base', 'cutoff_score': 0.1},
        {'model_name': 'jinaai/jina-reranker-v2-base-multilingual', 'cutoff_score': 0.1},
    ]

    for reranker in defaul_rerankers:
        existing_reranker = RerankerModel.objects.filter(model_name=reranker['model_name']).first()
        if not existing_reranker:
            new_reranker = RerankerModel(
                model_name=reranker['model_name'],
                cutoff_score=reranker['cutoff_score']
            )
            new_reranker.save()

    return render(request, 'home.html', {'datasets': datasets})