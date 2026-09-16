import os
import pickle
import numpy as np


_RF_HYBRID_ARTIFACT = None


def _get_rf_hybrid_artifact():
    global _RF_HYBRID_ARTIFACT
    if _RF_HYBRID_ARTIFACT is not None:
        return _RF_HYBRID_ARTIFACT

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    model_rel_path = os.path.join('data', 'random_forest_models', 'random_forest_hybrid_model_base.pkl')
    candidate_paths = [
        os.path.join(repo_root, model_rel_path),
        os.path.join(os.getcwd(), model_rel_path),
        os.path.join('/code', model_rel_path),
    ]

    for model_path in candidate_paths:
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                _RF_HYBRID_ARTIFACT = pickle.load(f)
            return _RF_HYBRID_ARTIFACT

    raise FileNotFoundError('random_forest_hybrid_model_base.pkl not found in expected paths')


def _safe_stats(values):
    if not values:
        return 0.0, 0.0, 0.0, 0.0
    arr = np.array(values, dtype=float)
    return float(np.mean(arr)), float(np.max(arr)), float(np.min(arr)), float(np.std(arr))


def predict_hallucination_index(vector_scores, bm25_scores, sources, rerank_sentiments):
    vector_scores_answer_mean, vector_scores_answer_max, vector_scores_answer_min, vector_scores_answer_std = _safe_stats(vector_scores)
    bm25_scores_answer_mean, bm25_scores_answer_max, bm25_scores_answer_min, bm25_scores_answer_std = _safe_stats(bm25_scores)

    vector_scores_question = [float(source.vector_score) for source in sources if source.vector_score is not None]
    bm25_scores_question = [float(source.bm25_score) for source in sources if source.bm25_score is not None]
    reranked_scores_question = [float(source.rerank_score) for source in sources if source.rerank_score is not None]

    vector_scores_question_mean, vector_scores_question_max, vector_scores_question_min, vector_scores_question_std = _safe_stats(vector_scores_question)
    bm25_scores_question_mean, bm25_scores_question_max, bm25_scores_question_min, bm25_scores_question_std = _safe_stats(bm25_scores_question)
    reranked_score_question_mean, reranked_score_question_max, reranked_score_question_min, reranked_score_question_std = _safe_stats(reranked_scores_question)

    contradiction_count = 0
    entailment_count = 0
    for sentiment in rerank_sentiments:
        if isinstance(sentiment, (list, tuple)) and len(sentiment) > 0:
            label = str(sentiment[0]).lower()
        else:
            label = str(sentiment).lower()
        if label == 'contradiction':
            contradiction_count += 1
        elif label == 'entailment':
            entailment_count += 1

    rf_features = [
        vector_scores_answer_mean,
        bm25_scores_answer_mean,
        vector_scores_question_mean,
        bm25_scores_question_mean,
        reranked_score_question_mean,
        vector_scores_answer_max,
        bm25_scores_answer_max,
        vector_scores_answer_min,
        bm25_scores_answer_min,
        vector_scores_answer_std,
        bm25_scores_answer_std,
        vector_scores_question_max,
        bm25_scores_question_max,
        reranked_score_question_max,
        vector_scores_question_min,
        bm25_scores_question_min,
        reranked_score_question_min,
        vector_scores_question_std,
        bm25_scores_question_std,
        reranked_score_question_std,
        contradiction_count,
        entailment_count,
    ]

    artifact = _get_rf_hybrid_artifact()
    model = artifact['model']
    X_new = np.array([rf_features], dtype=float)
    proba = model.predict_proba(X_new)[:, 1]
    return round(float(proba[0])*100, 0) if len(proba) else 0
