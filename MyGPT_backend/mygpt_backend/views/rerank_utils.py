from sentence_transformers import CrossEncoder
from ..models import RerankerModel
import os
import torch


def _load_cross_encoder(model_name_or_path, trust_remote_code=False):
    """Load CrossEncoder while applying tokenizer regex fix for affected Mistral tokenizers."""
    try:
        return CrossEncoder(
            model_name_or_path,
            trust_remote_code=trust_remote_code,
            processor_kwargs={"fix_mistral_regex": True},
            activation_fn=torch.nn.Sigmoid()
        )
    except TypeError:
        # Backward compatibility for sentence-transformers versions without tokenizer_args.
        return CrossEncoder(model_name_or_path, trust_remote_code=trust_remote_code)

def rerank_sources(sources, question_text, reranker, language_of_docs='english'):

    if reranker == 'default' and language_of_docs == 'english':
        reranker = 'cross-encoder/qnli-electra-base'
    elif reranker == 'default' and language_of_docs != 'english':
        reranker = 'cross-encoder/mmarco-mMiniLMv2-L12-H384-v1'
    reranker_model = RerankerModel.objects.filter(model_name__contains=reranker).first()
    if not reranker_model:
        if language_of_docs == 'english':
            reranker_model_name = 'cross-encoder/qnli-electra-base'
            cutoff_score = 0.1
        else:
            reranker_model_name = 'cross-encoder/mmarco-mMiniLMv2-L12-H384-v1'
            cutoff_score = 0.05
        # default to cross-encoder/qnli-electra-base
        reranker_model = RerankerModel.objects.filter(model_name=reranker_model_name).first()
        if not reranker_model:
            # create the default reranker model
            reranker_model = RerankerModel(
                model_name=reranker_model_name,
                cutoff_score=cutoff_score
            )
            reranker_model.save()
    
    # rerank the sources based on vector score + bm25 score using cross encoder
    # cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    # check if model is available locally. if not, download and save it
    reranker_name = reranker_model.model_name.split('/')[-1]
    reranker_full_name = reranker_model.model_name
    cross_encoder_path = f'/code/data/reranker/{reranker_name}'
    try:
        # check if path exists
        if not os.path.exists(cross_encoder_path):
            raise FileNotFoundError
        else:
            cross_encoder = _load_cross_encoder(cross_encoder_path)
    except:
        cross_encoder = _load_cross_encoder(reranker_full_name)
        cross_encoder.save_pretrained(f'/code/data/reranker/{reranker_name}')

    RERANK_SCORE_THRESHOLD = reranker_model.cutoff_score

    # cross_encoder_path = '/code/data/reranker/zerank_2'
    # try:
    #     cross_encoder = CrossEncoder(cross_encoder_path)
    # except:
    #     cross_encoder = CrossEncoder('zeroentropy/zerank-2', trust_remote_code=True)
    #     cross_encoder.save_pretrained('/code/data/reranker/zerank_2')

    # RERANK_SCORE_THRESHOLD = 0.3

    reranked_sources = []
    for source in sources:
        source_text = source['context']
        score = cross_encoder.predict([[question_text, source_text]])[0]
        score_rounded = round(float(score), 3)
        source['reranked_score'] = score_rounded
        if score_rounded > RERANK_SCORE_THRESHOLD:
            reranked_sources.append(source)
    
    # sort the sources based on the cross encoder score and combined score
    reranked_sources.sort(key=lambda x: x['reranked_score'], reverse=True)

    # add rank to each source
    for idx, source in enumerate(reranked_sources):
        source['rank'] = idx + 1

    # return the reranked sources
    return reranked_sources

def rerank_answer_sources(sources, answer_text):
    # rerank the sources based on vector score + bm25 score using cross encoder

    # check if model is available locally. if not, download and save it
    cross_encoder_path = '/code/data/reranker/cross_encoder_nli_deberta_v3_base'
    try:
        cross_encoder = _load_cross_encoder(cross_encoder_path)
    except:
        cross_encoder = _load_cross_encoder('cross-encoder/nli-deberta-v3-base')
        cross_encoder.save_pretrained('/code/data/reranker/cross_encoder_nli_deberta_v3_base')

    reranked_scores = []
    for source in sources:
        scores = cross_encoder.predict([(answer_text, source)])
        label_mapping = ['contradiction', 'entailment', 'neutral']
        max_index = int(scores.argmax())
        label = [label_mapping[max_index]]
        # score_rounded = round(float(score), 3)
        reranked_scores.append(label)

    # return the reranked sources
    return reranked_scores