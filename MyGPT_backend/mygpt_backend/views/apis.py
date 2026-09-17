from django.core.files.base import File
from django.http import StreamingHttpResponse, FileResponse, Http404
from django.conf import settings
from django.utils._os import safe_join
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.utils.timezone import make_aware
from django.core import serializers
import numpy as np
import chromadb
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
import datetime
import logging
import os
import shutil
import json
import re
from ollama import Client as OllamaClient, ListResponse
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)

from .bm25_utils import (
    retrieve_chunks_by_bm25, 
    hybrid_source_combination,
    get_answer_distance_by_context_bm25 
)

# Import from specialized modules
from .helpers import (
    safe_path,
    sanitize_filename,
    seconds_to_hhmmss,
    min_max_normalization,
    validate_dataset_name,
)

from .document_processing import (
    highlight_pdf,
)

from .embedding_utils import (
    get_embedding_model_ef,
    add_embeddings_to_qna
)

from .vector_db import (
    nearestDataChroma,
    get_answer_distance,
    get_answer_distance_by_context
)

from .analytics import (
    add_pca_to_qna_and_dataset,
    get_relevance_score
)

from .dataset_management import (
    add_demo_dataset
)

from .rerank_utils import (
    rerank_answer_sources
)

from .HI_prediction_by_random_forest import predict_hallucination_index

from ..models import Papers, Videos, Dataset, chunks, Question, Answer, Source, Conversation, Model, EmbeddingModel, FrontEndSettings, DisclaimerAgreement, PaperSections

####################
# APIs             #
####################

@api_view(['POST'])
def get_datasets(request):
    if request.method == 'POST':
        json_request = JSONParser().parse(request)
        user_email = json_request['user_email']
        user_group = json_request['user_group']
        if user_email == '':
            datasets = Dataset.objects.filter(user_email='-', user_group='user')
        elif user_group != '' and user_group != 'user' and user_email != '':
            group_datasets = Dataset.objects.filter(user_group=user_group)
            email_datasets = Dataset.objects.filter(user_email=user_email)
            # combine datasets
            datasets = group_datasets | email_datasets
        else:
            datasets = Dataset.objects.filter(user_email=user_email)
        datasets_ = serializers.serialize('json', datasets)
        datasets_json = json.loads(datasets_)
        datasets = []
        for dataset in datasets_json:
            datasets.append(dataset['fields'])
        # sort datasets alphabetically
        datasets = sorted(datasets, key=lambda x: x['dataset_name'])
        return Response(datasets)

def resolve_dataset_for_user(dataset_name, user_email, user_group):
    if user_email == '':
        return Dataset.objects.get(dataset_name=dataset_name, user_email='-')

    dataset_count = Dataset.objects.filter(dataset_name=dataset_name, user_email=user_email).count()
    if dataset_count == 0 and user_group != '' and user_group != 'user':
        return Dataset.objects.get(dataset_name=dataset_name, user_group=user_group)

    return Dataset.objects.get(dataset_name=dataset_name, user_email=user_email)


@api_view(['POST'])
def get_dataset_details(request):
    if request.method == 'POST':
        json_request = JSONParser().parse(request)
        dataset_name = json_request['dataset']
        user_email = json_request['user_email']
        user_group = json_request['user_group']

        dataset = resolve_dataset_for_user(dataset_name, user_email, user_group)
        dataset_json = serializers.serialize('json', [dataset])
        dataset_fields = json.loads(dataset_json)[0]['fields']
        return Response(dataset_fields)

@api_view(['POST'])
def update_dataset(request):
    if request.method == 'POST':
        json_request = JSONParser().parse(request)
        dataset_name = json_request.get('dataset', '')

        if not dataset_name:
            return Response({'saved': False, 'error': True, 'error_message': 'Dataset name is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            dataset = Dataset.objects.get(dataset_name=dataset_name)
        except Dataset.DoesNotExist:
            return Response({'saved': False, 'error': True, 'error_message': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)

        if 'system_prompt' in json_request:
            dataset.dataset_prompt = json_request['system_prompt']
        if 'Qsem_a' in json_request:
            dataset.coefficient_a_Qsem = json_request['Qsem_a']
        if 'Qkey_b' in json_request:
            dataset.coefficient_b_Qkey = json_request['Qkey_b']
        if 'Qrank_c' in json_request:
            dataset.coefficient_c_Qrank = json_request['Qrank_c']
        if 'Asem_x' in json_request:
            dataset.coefficient_x_Asem = json_request['Asem_x']
        if 'Akey_y' in json_request:
            dataset.coefficient_y_Akey = json_request['Akey_y']
        if 'Arank_z' in json_request:
            dataset.coefficient_z_Arank = json_request['Arank_z']
        if 'QRS_p' in json_request:
            dataset.coefficient_p_QRS = json_request['QRS_p']
        if 'ARS_q' in json_request:
            dataset.coefficient_q_ARS = json_request['ARS_q']
        if 'HI_by_equation' in json_request:
            dataset.HI_by_equation = json_request['HI_by_equation']

        dataset.save()

        dataset_json = serializers.serialize('json', [dataset])
        dataset_fields = json.loads(dataset_json)[0]['fields']
        return Response({'saved': True, 'dataset': dataset_fields}, content_type="application/json")

@api_view(['POST'])
def get_documents(request):
    if request.method == 'POST':
        json_request = JSONParser().parse(request)
        dataset_name = json_request['dataset']
        user_email = json_request['user_email']
        user_group = json_request['user_group']
        dataset = resolve_dataset_for_user(dataset_name, user_email, user_group)

        papers = Papers.objects.filter(paper_dataset=dataset).order_by('paper_date_time')
        if papers.count() > 0:
                dataset_type = 'papers'
                docs_ = serializers.serialize('json', papers)
        else:
            videos = Videos.objects.filter(video_dataset=dataset).order_by('video_date_time')
            if videos.count() > 0:
                dataset_type = 'videos'
                docs_ = serializers.serialize('json', videos)
        docs_json = json.loads(docs_)
        documents = []
        for doc in docs_json:
            documents.append(doc['fields'])
        # sort documents alphabetically
        if dataset_type == 'videos':
            documents = sorted(documents, key=lambda x: x['video_title'])
        else:
            documents = sorted(documents, key=lambda x: x['paper_title'])
        return Response({'documents': documents, 'dataset_type': dataset_type})

# example json: {"text": "how many inactive conformational states ABL1 has?", "dataset": "ABL1"}
@api_view(['POST'])
def get_context(request):
    if request.method == 'POST':
        json_request = JSONParser().parse(request)
        question_text = json_request['text']
        model = json_request['model_type']
        skip_highlight = True
        model_exist = Model.objects.filter(model_name=model).exists()
        if not model_exist:
            Model.objects.create(model_name=model, model_size='3GB')
        model_type = Model.objects.get(model_name=model)
        dataset_name = json_request['dataset']
        # document_title = json_request['document_title'] if 'document_title' in json_request else ''
        focused_document_titles = json_request['focused_document_titles'] if 'focused_document_titles' in json_request else []
        focused_section = json_request['focused_section'] if 'focused_section' in json_request else ''
        use_default_qrs = json_request['use_default_qrs']
        question_best_distance = json_request['question_best_distance']
        question_worst_distance = json_request['question_worst_distance']
        maximum_chunks_count = json_request['maximum_chunks_count']
        no_cutoff = json_request['no_cutoff']

        # best and worst scores for BM25
        best_bm25_score = 20
        worst_bm25_score = 0

        semantic_score = 0
        keyword_score = 0
        rerank_score = 0
        relevance_score = 0
        weight_a_default = 4 
        weight_b_default = -4
        weight_c_default = -1
        relevance_score_min = -5.5
        relevance_score_max = 3.03

        # check if dataset exists or crate a new one
        dataset_exist = Dataset.objects.filter(dataset_name=dataset_name).exists()
        if not dataset_exist:
            Dataset.objects.create(
                dataset_name=dataset_name,
                library_type='papers',
                dataset_size=0,
                dataset_date_time=make_aware(datetime.datetime.now()),
                user_email='-',
                coefficient_a_Qsem = weight_a_default,
                coefficient_b_Qkey = weight_b_default,
                coefficient_c_Qrank = weight_c_default,
            )
        dataset = Dataset.objects.get(dataset_name=dataset_name)
        embedding_model = dataset.embedding_model
        new_conversation = json_request['new_conversation']
        previous_question = json_request['previous_query']
        no_context = json_request['no_context']
        use_bm25 = dataset.use_bm25 if hasattr(dataset, 'use_bm25') else False
        reranker = dataset.reranker if hasattr(dataset, 'reranker') else 'None'
        use_reranker = False if reranker == 'None' else True
        weight_a = dataset.coefficient_a_Qsem if hasattr(dataset, 'coefficient_a_Qsem') else weight_a_default
        weight_b = dataset.coefficient_b_Qkey if hasattr(dataset, 'coefficient_b_Qkey') else weight_b_default
        weight_c = dataset.coefficient_c_Qrank if hasattr(dataset, 'coefficient_c_Qrank') else weight_c_default
        language_of_docs = dataset.documents_language if hasattr(dataset, 'documents_language') else 'english'
        keywords = json_request['keywords'] if 'keywords' in json_request else ''
        translated_text = json_request['translated_text'] if language_of_docs != 'english' and 'translated_text' in json_request else ''

        if no_context:    
            titles, pages, starts, stops, chunks_txt, distances, reranked_scores = [], [], [], [], [], [], []
            vector_sources = []
            bm25_sources = []
            relevance_score = 0
            semantic_score = 0
            keyword_score = 0
            rerank_score = 0
            normalized_distances = []
        else:
            titles, pages, starts, stops, chunks_txt, distances, reranked_scores = nearestDataChroma(translated_text if translated_text else question_text, dataset_name, focused_document_titles, focused_section, keywords, embedding_model, maximum_chunks_count, no_cutoff, reranker, language_of_docs)
            vector_sources = []
            distances = [round(dist, 3) for dist in distances]
            semantic_score, normalized_distances = get_relevance_score(distances, embedding_model, True, use_default_qrs, question_best_distance, question_worst_distance)

            bm25_sources = []
            if use_bm25:
                # get similar chunks using BM25
                results, scores = retrieve_chunks_by_bm25(translated_text if translated_text else question_text, dataset_name, focused_document_titles, maximum_chunks_count, reranker, language_of_docs)
                # results, scores = retrieve_chunks_by_bm25(question_text, dataset_name, document_title, 3, reranker)
                normalized_scores = min_max_normalization(scores, best_bm25_score, worst_bm25_score, False)
                for idx, result in enumerate(results):
                    cleaned_chunk = re.sub(r'\s+', ' ', str(result['text']))
                    # remove all new lines
                    cleaned_chunk = re.sub(r'\n+', ' ', cleaned_chunk)
                    chunk_split = cleaned_chunk.split('; ', 2)
                    document_title = chunk_split[0].replace('document ', '')
                    page = chunk_split[1].replace('page ', '')
                    chunk_txt = chunk_split[2]
                    bm25_sources.append({
                        'document': document_title,
                        'page': int(page),
                        'context': chunk_txt,
                        'bm25_score_raw': round(float(scores[idx]),2),
                        'bm25_score': round(normalized_scores[idx], 3),
                        'vector_score': 0,
                        'rank': idx + 1,
                        'reranked_score': result.get('reranked_score', 0),
                        'vector_distance_raw': 0,
                    })
                # get average BM25 score for sources
                keyword_score = round(sum([source['bm25_score'] for source in bm25_sources]) / len(bm25_sources) if bm25_sources else 0, 2)
        # library_type = 'papers' if len(pages) else 'videos'
        library_type = 'papers'

        # if no_context is true, create or get dataset
        if no_context:
            dataset_name = model + '_direct_chat'
            dataset_exist = Dataset.objects.filter(dataset_name=dataset_name).exists()
            if not dataset_exist:
                dataset = Dataset.objects.create(
                    dataset_name=dataset_name,
                    library_type='papers',
                    dataset_size=0,
                    dataset_date_time=make_aware(datetime.datetime.now()),
                    direct_chat_without_docs = True,
                    user_email='-'
                )

        # save question to database
        current_date_time = make_aware(datetime.datetime.now())
        dataset = Dataset.objects.get(dataset_name=dataset_name)
        question_text = question_text.split('<tool_response>')[0]
        question_exist = Question.objects.filter(question_dataset=dataset).filter(question_text=question_text).filter(model_type=model_type).exists()
        if question_exist:
            questions = Question.objects.filter(question_text=question_text, model_type=model_type, question_dataset=dataset)
            question = questions[0]
            question.keywords = keywords
            question.relevance_score = semantic_score if semantic_score <= 100 else 100
            question.save()
            conversation_id = question.conversation.id
            conversation = Conversation.objects.get(id=conversation_id)
        else:
            if (new_conversation):
                conversation = Conversation.objects.create(
                    question_answer_count=1,
                    conversation_dataset=dataset,
                    start_date_time=current_date_time
                )
            else:
                questions = Question.objects.filter(question_text=previous_question, question_dataset=dataset)
                if questions.count() == 0:
                    return Response({'error':True, 'error_message':'Previous question not found'}, content_type="application/json")
                else:
                    question = questions[0]
                conversation_id =  question.conversation.id
                conversation = Conversation.objects.get(id=conversation_id)
                conversation.question_answer_count += 1
                conversation.save()
            question = Question.objects.create(
                question_text=question_text,
                translated_question_text=translated_text if translated_text else '',
                relevance_score=semantic_score if semantic_score <= 100 else 100,
                model_type=model_type,
                keywords=keywords,
                question_dataset=dataset,
                qrs_lower_range=question_best_distance,
                qrs_upper_range=question_worst_distance,
                conversation=conversation,
                saved_date_time=current_date_time
            )
        
        # add embeddings to question
        if not no_context:
            add_embeddings_to_qna(question_text, 'question', embedding_model)

        for idx, title in enumerate(titles):
            # filter distances if normalized_distances are less than 0.1
            if normalized_distances[idx] < 0.1:
                continue
            vector_sources.append({
                'document': title,
                'page': pages[idx] if library_type == 'papers' else '',
                'start': seconds_to_hhmmss(starts[idx]) if library_type == 'videos' else '',
                'stop': seconds_to_hhmmss(stops[idx]) if library_type == 'videos' else '',
                'context': str(chunks_txt[idx]),
                'vector_distance_raw': round(distances[idx],3), #round to 3 decimals,
                'vector_score': round(normalized_distances[idx],3),
                'rank': idx + 1,
                'reranked_score': reranked_scores[idx] if use_reranker else 0,
                'bm25_score_raw': 0,
                'bm25_score': 0,
                'bm25_rank': 0
            })

        # combine vector_sources and bm25_sources
        reranked_sources = hybrid_source_combination(vector_sources, bm25_sources)
        
        # get average reranked score for sources
        rerank_score = round(sum([source['reranked_score'] for source in reranked_sources]) / len(reranked_sources) if reranked_sources else 0, 2)

        # calcuate relevance score based on semantic_score, keyword_score and rerank_score with weights determined by sensitivity analysis
        relevance_score_raw = round((semantic_score/100 * weight_a) + (keyword_score * weight_b) + (rerank_score * weight_c), 2)
        # normalize relevance score to be between 0 and 100 with min-max normalization using relevance_score_min and relevance_score_max
        relevance_score = round(min_max_normalization([relevance_score_raw], relevance_score_max, relevance_score_min, False)[0] * 100, 0)

        # reranked sources based on vector_score + bm25_score
        # reranked_sources = rerank_sources(combined_sources, question_text)

        sources_grouped = []
        for source in reranked_sources:
            if len(sources_grouped) == 0:
                sources_grouped.append([source])
            else:
                found = False
                for source_group in sources_grouped:
                    if source['document'] == source_group[0]['document']:
                        source_group.append(source)
                        found = True
                        break
                if not found:
                    sources_grouped.append([source])

        # hightlight pdf with source paper and page
        if library_type == 'papers' and not skip_highlight:
            for source_grp in sources_grouped:
                paper_obj = Papers.objects.filter(paper_dataset=dataset).filter(paper_title=source_grp[0]['document'])[0].paper_attachment
                if (len(paper_obj.path.split('/')[-1].split('_')) > 1): 
                    paper_name =   paper_obj.path.split('/')[-1].split('_')[0] + '.pdf'
                else:
                    paper_name =   paper_obj.path.split('/')[-1]
                print("paper_name: " + paper_name)
                original_pdf_path = 'data/pdfs/'+ dataset_name + '/' + paper_name
                highlighted_pdf_path = 'data/pdfs/' + dataset_name + '/' + paper_name.split('.')[0] + '_highlighted.pdf'

                # get all files with output_file name in thier name
                files = [f for f in os.listdir('data/pdfs') if (paper_name.split('.')[0] + '_highlighted.pdf') in f]
                # remove all files with output_file name in thier name
                for f in files:
                    # check for the path traversal attack
                    if f.endswith('.pdf') and os.path.exists('data/pdfs/' + f):
                        safe_filename = sanitize_filename(f)
                        safe_path = os.path.join('data/pdfs', safe_filename)
                        if os.path.exists(safe_path) and os.path.isfile(safe_path):
                            os.remove(safe_path)
                if original_pdf_path.endswith('.pdf'):
                    highlight_pdf(
                        original_pdf_path, 
                        highlighted_pdf_path, 
                        source_grp
                    )

                    # create highlighted paper object
                    paper = Papers.objects.filter(paper_dataset=dataset).filter(paper_title=source_grp[0]['document'])[0]
                    with open(highlighted_pdf_path, 'rb') as f:
                        # paper.paper_attachment.save(dataset_name + '/' + paper_name.split('.')[0] + '_highlighted.pdf', File(f), save=True)
                        paper.highlighted_attachment.save(dataset_name + '/' + paper_name.split('.')[0] + '_highlighted.pdf', File(f), save=True)
        
        full_context = ''
        if question_exist:
            # delete previous sources
            Source.objects.filter(question=question).delete()
        for idx, source in enumerate(reranked_sources):
            sanitized_context = str(source.get('context', '')).replace("\x00", "\uFFFD")
            chunk = chunks.objects.filter(chunk_text=sanitized_context, chunk_dataset=dataset)
            Source.objects.create(
                source_doc=source['document'],
                source_pointer=source['page'] if library_type == 'papers' else source['start'],
                context=sanitized_context,
                vector_distance_raw=source.get('vector_distance_raw', 0),
                vector_score=source.get('vector_score', 0),
                bm25_score_raw=source.get('bm25_score_raw', 0),
                bm25_score=source.get('bm25_score', 0),
                rank=source.get('rank', 0),
                rerank_score=source.get('reranked_score', 0),
                secondary_rank=source.get('bm25_rank', 0),
                question=question,
                chunk=chunk[0] if chunk.count() else None
            )
            full_context += sanitized_context + "\n\n"
            # Determine the color code based on distance or score
            if (source.get('vector_score', 0) > 0.5) or (source.get('bm25_score', 0) > 0.5):
                source['color_code'] = 'green'
            elif (source.get('vector_score', 0) > 0.3) or (source.get('bm25_score', 0) > 0.3):
                source['color_code'] = 'yellow'
            elif (source.get('vector_score', 0) > 0.15) or (source.get('bm25_score', 0) > 0.15):
                source['color_code'] = 'red'
            else:
                source['color_code'] = 'gray'

        # combine the vector_scores and bm25_scores and sort them from high to low
        # combined_sources = sorted(combined_sources, key=lambda x: (x['vector_score'] if 'vector_score' in x else 0) + (x['bm25_score'] if 'bm25_score' in x else 0), reverse=True)

        # sort reranked sources by vector_score, then by bm25_score
        reranked_sources = sorted(reranked_sources, key=lambda x: (x['vector_score'] if 'vector_score' in x else 0) + (x['bm25_score'] if 'bm25_score' in x else 0), reverse=True)

        question.semantic_score = semantic_score if semantic_score <= 100 else 100
        question.keyword_score = keyword_score*100 if keyword_score <= 1 else 100
        question.rerank_score = rerank_score*100 if rerank_score <= 1 else 100
        question.relevance_score = relevance_score if relevance_score <= 100 else 100
        question.save()

        context_json = {
            'context': full_context,
            'relevance_score': relevance_score if relevance_score <= 100 else 100,
            'semantic_score': semantic_score if semantic_score <= 100 else 100,
            'keyword_score': keyword_score*100,
            'rerank_score': rerank_score*100,
            'sources': reranked_sources if not no_context else []
        }
        
        return Response(context_json, content_type="application/json")
    
@api_view(['GET'])
def get_conversations_by_dataset(request):
    if request.method == 'GET':
        dataset_name = request.GET.get('dataset')
        dataset = Dataset.objects.get(dataset_name=dataset_name)
        conversations = Conversation.objects.filter(conversation_dataset=dataset)
        conversations_obj = []
        for conversation in conversations:
            conversation_id = conversation.id
            questions = Question.objects.filter(conversation=conversation).order_by('saved_date_time')
            conversation_json = {}
            conversation_json['conversation_id'] = conversation_id
            conversation_json['questions_answers'] = []
            for question in questions:
                # if answewr count is 0, skip the question
                answer_count = Answer.objects.filter(question=question).count()
                if answer_count == 0:
                    continue
                # answers = Answer.objects.filter(question=question)
                qna_json = {
                    'question_id': question.id,
                    'question': question.question_text,
                    # 'answers': answers[0].answer_text,
                    'relevance_score': question.relevance_score
                }
                conversation_json['questions_answers'].append(qna_json)
            conversations_obj.append(conversation_json)
        return Response({'conversations':conversations_obj})

@api_view(['GET'])
def get_question_details(request):
    if request.method == 'GET':
        question_id = request.GET.get('question_id')
        question = Question.objects.get(id=question_id)
        answers = Answer.objects.filter(question=question)
        sources = Source.objects.filter(question=question)
        sources_json = []
        for source in sources:
            sources_json.append({
                'paper': source.source_doc,
                'page': source.source_pointer,
                'context': source.context,
                'vector_distance_raw': source.vector_distance_raw,
                'vector_score': source.vector_score,
                'bm25_score_raw': source.bm25_score_raw,
                'bm25_score': source.bm25_score,
                'rerank_score': source.rerank_score,
                'rank': source.rank,
                'secondary_rank': source.secondary_rank,
            })
        # check if sources has rank, if yes, sort by rank or sort sources by vector_score and bm25_score
        if (len(sources_json) > 0 and sources_json[0]['rank'] != 0):
            sources_json = sorted(sources_json, key=lambda x: x['rank'])
        else:
            sources_json = sorted(sources_json, key=lambda x: (x['vector_score'] if 'vector_score' in x else 0) + (x['bm25_score'] if 'bm25_score' in x else 0), reverse=True)
        answers_json = []
        for answer in answers:
            answers_json.append({
                'answer': answer.answer_text,
                'relevance_score': answer.relevance_score,
                'hallucination_index_by_equation': answer.hallucination_index_by_equation,
                'hallucination_index_by_ml': answer.hallucination_index_by_ml,
                'answer_no_context': answer.answer_no_context_text,
                'rating': answer.rating,
                'rating_comment': answer.user_comment,
            })
        # Determine the color code based on distance or score
        for source in sources_json: 
            if (source['vector_score'] != 0 and source['vector_score'] > 0.5) or (source['bm25_score'] != 0 and source['bm25_score'] > 0.5):
                source['color_code'] = 'green'
            elif (source['vector_score'] != 0 and source['vector_score'] > 0.3) or (source['bm25_score'] != 0 and source['bm25_score'] > 0.3):
                source['color_code'] = 'yellow'
            elif (source['vector_score'] != 0 and source['vector_score'] > 0.15) or (source['bm25_score'] != 0 and source['bm25_score'] > 0.15):
                source['color_code'] = 'red'
            else:
                source['color_code'] = 'gray'
        question_json = {
            'question': question.question_text,
            'relevance_score': question.relevance_score,
            'ground_truth': question.ground_truth,
            'question_type': question.question_type,
            'keywords': question.keywords,
            'llm': question.model_type.model_name,
            'answers': answers_json,
            'sources': sources_json
        }
        return Response(question_json)
    
@api_view(['POST'])
def save_answer(request):
    if request.method == 'POST':
        json_request = JSONParser().parse(request)
        question_text = json_request['question_text']
        answer_text = json_request['answer_text']
        translated_answer_text = json_request['translated_answer_text'] if 'translated_answer_text' in json_request else ''
        answer_no_context_text = json_request['answer_no_context_text']
        model = json_request['model_type']
        model_type = Model.objects.get(model_name=model)
        dataset_name = json_request['dataset']
        dataset = Dataset.objects.get(dataset_name=dataset_name)
        use_bm25 = dataset.use_bm25 if hasattr(dataset, 'use_bm25') else False
        language_of_docs = dataset.documents_language if hasattr(dataset, 'documents_language') else 'english'
        question = Question.objects.get(question_text=question_text, model_type=model_type, question_dataset=dataset)
        embedding_model = dataset.embedding_model
        no_context = json_request['no_context']
        
        best_distance_a_r = json_request['answer_best_distance']
        worst_distance_a_r = json_request['answer_worst_distance']
        use_default_ars = json_request['use_default_ars']
        
        QRS_p_r = json_request['QRS_p']
        ARS_q_r = json_request['ARS_q']
        # HI_by_equation = json_request['HI_by_equation']
        use_default_hi = json_request['use_default_hi']
        temperature = json_request['temperature']
        top_k = json_request['top_k']
        top_p = json_request['top_p']

        # get context from sources
        sources = Source.objects.filter(question=question)
        all_contexts = [source.context for source in sources]
        sources_ranks = [source.rank for source in sources]
        # vector_contexts = []
        vector_distances = []
        vector_scores = []
        # bm25_contexts = []
        bm25_scores_raw = []
        bm25_scores = []
        rerank_sentiments = []
        # bm25_rerank_scores = []

        # best and worst scores for BM25
        best_bm25_score = 20
        worst_bm25_score = 0

        relevance_score_min = -6.42
        relevance_score_max = 3.65
        weight_x = dataset.coefficient_x_Asem if hasattr(dataset, 'coefficient_x_Asem') else 5
        weight_y = dataset.coefficient_y_Akey if hasattr(dataset, 'coefficient_y_Akey') else -2
        weight_z = dataset.coefficient_z_Arank if hasattr(dataset, 'coefficient_z_Arank') else 0

        semantic_score = 0
        keyword_score = 0
        rerank_score = 0
        relevance_score = 0

        # for source in sources:

            # if source.vector_distance_raw != 0:
            #     vector_contexts.append(source.context)
            # if source.bm25_score_raw != 0:
            #     bm25_contexts.append(source.context)
        
        if not no_context:
            distances = get_answer_distance_by_context(answer_no_context_text, dataset_name, all_contexts, embedding_model)

            if distances is None or len(distances) == 0:
                mean_distance_a = 0
                semantic_score = 0
            else:
                distances = [round(dist, 3) for dist in distances]
                distances_a = get_answer_distance_by_context(translated_answer_text if translated_answer_text else answer_text, dataset_name, all_contexts, embedding_model)
                distances_a = [round(dist, 3) for dist in distances_a]
                vector_distances = distances_a

                mean_distance_a = round((sum(distances_a) / len(distances_a)), 3)

            rerank_sentiments = []
            if language_of_docs == 'english':
                rerank_sentiments = rerank_answer_sources(all_contexts, translated_answer_text if translated_answer_text else answer_text)

            if use_bm25:
                try:
                    bm25_docs, bm25_scores_raw = get_answer_distance_by_context_bm25(translated_answer_text if translated_answer_text else answer_text, all_contexts, language_of_docs)
                    # round bm25_scores to 3 decimals
                    bm25_scores_raw = [round(float(score), 3) for score in bm25_scores_raw]
                    bm25_scores = min_max_normalization(bm25_scores_raw, best_bm25_score, worst_bm25_score, False)
                    # round to 3 decimals
                    bm25_scores = [round(score, 3) for score in bm25_scores]
                    keyword_score = round(sum(bm25_scores) / len(bm25_scores) * 100, 2) if bm25_scores else 0
                except Exception as e:
                    print('Error in BM25 answer distance: ', e)
                    bm25_scores = []

                # bm25_rerank_scores = rerank_answer_sources(all_contexts, answer_text)
                    
                # extra_score = round((sum(bm25_scores) / len(bm25_scores)), 3)
                # mean_distance_a += extra_score
        else:
            mean_distance_a = 0
            semantic_score = 0

        #  calculate answer relevance score
        if use_default_ars and not no_context:
            best_distance_a = 0
            worst_distance_a = 0

            embedding_model_obj = EmbeddingModel.objects.get(model_name=embedding_model)
            best_distance_a = embedding_model_obj.best_distance_ac
            worst_distance_a = embedding_model_obj.worst_distance_ac

            buffer_distance = 0.05 * (worst_distance_a - best_distance_a)
            best_distance_a = best_distance_a - buffer_distance
            worst_distance_a = worst_distance_a + buffer_distance
        else:
            best_distance_a = best_distance_a_r
            worst_distance_a = worst_distance_a_r

        # if embedding_model == 'nomic-embed-text:latest':
        #     best_distance_a = -180
        #     worst_distance_a = 120
        # elif embedding_model == 'multi-qa-MiniLM-L6-cos-v1':
        #     best_distance_a = -0.8
        #     worst_distance_a = 0.8
        # elif embedding_model == 'multi-qa-MiniLM-L6-v2':
        #     best_distance_a = -1
        #     worst_distance_a = 1.4
        # else:
        #     best_distance_a = -1
        #     worst_distance_a = 1.4

        vector_scores = min_max_normalization(vector_distances, best_distance_a, worst_distance_a, False)
        # round to 3 decimals
        vector_scores = [round(score, 3) for score in vector_scores]
        semantic_score = round(sum(vector_scores) / len(vector_scores) * 100, 2) if vector_scores else 0

        # relevance_score = round(((1 - ((mean_distance_a - best_distance_a) / (worst_distance_a - best_distance_a))) * 100),0)

        # get relevance score based on semantic_score, keyword_score and rerank_score with weights determined by sensitivity analysis
        relevance_score_raw = round((semantic_score/100 * weight_x) + (keyword_score/100 * weight_y) + (rerank_score/100 * weight_z), 2)
        relevance_score = round(min_max_normalization([relevance_score_raw], relevance_score_max, relevance_score_min, False)[0] * 100, 0)
        if relevance_score < 0:
            relevance_score = 0
        elif relevance_score > 100:
            relevance_score = 100
        question_relevance_score = question.relevance_score

        # caclulate hallucination index
        if use_default_hi:
            QRS_p = 1
            ARS_q = 2
        else:
            QRS_p = QRS_p_r
            ARS_q = ARS_q_r
        maxHI = 0.8
        minHI = 0.2

        if(question_relevance_score == 0):
            hallucination_index_by_equation_raw = 1
            hallucination_index_by_equation = round((hallucination_index_by_equation_raw - minHI)/(maxHI - minHI) * 100, 0)
        else:
            # relevance scores are on a 0-100 scale; the equation expects 0-1 fractions
            question_relevance_fraction = question_relevance_score / 100
            answer_relevance_fraction = relevance_score / 100
            hallucination_index_by_equation_raw = 1 - ((QRS_p * question_relevance_fraction)/ (QRS_p + ARS_q)) - ((ARS_q * answer_relevance_fraction)/ (QRS_p + ARS_q))
            hallucination_index_by_equation = round((hallucination_index_by_equation_raw - minHI)/(maxHI - minHI) * 100, 0)

        # create new sources array with vector_distances and vector_scores
        new_sources = []
        for rank in sources_ranks:
            new_source = sources.filter(rank=rank).last()
            idx = sources_ranks.index(rank)
            new_source.vector_distance_answer_raw = vector_distances[idx] if len(vector_distances) > idx else 0
            new_source.vector_score_answer = vector_scores[idx] if len(vector_scores) > idx else 0
            new_source.bm25_score_raw_answer = bm25_scores_raw[idx] if len(bm25_scores_raw) > idx else 0
            new_source.bm25_score_answer = bm25_scores[idx] if len(bm25_scores) > idx else 0
            new_source.rerank_entailment = rerank_sentiments[idx][0] if len(rerank_sentiments) > idx else "unknown"
            new_source.save()
            new_sources.append(new_source)
            # convert to json serializable format
        new_sources_json = []
        for source in new_sources:
            new_sources_json.append({
                'paper': source.source_doc,
                'page': source.source_pointer,
                'context': source.context,
                'vector_distance_raw': source.vector_distance_raw,
                'vector_score': source.vector_score,
                'answer_vector_distance_raw': source.vector_distance_answer_raw,
                'answer_vector_score': source.vector_score_answer,
                'bm25_score_raw': source.bm25_score_raw,
                'bm25_score': source.bm25_score,
                'rerank_score': source.rerank_score,
                'rank': source.rank,
                'secondary_rank': source.secondary_rank,
                'answer_bm25_score': source.bm25_score_answer,
                'rerank_sentiment': source.rerank_entailment
            })

        hallucination_index_by_ml = 0
        try:
            hallucination_index_by_ml = predict_hallucination_index(vector_scores, bm25_scores, sources, rerank_sentiments)
        except Exception as e:
            print('Error calculating random forest hallucination probability:', e)
        
        Answer.objects.create(
            answer_text=answer_text,
            translated_answer_text=translated_answer_text if translated_answer_text else '',
            answer_no_context_text=answer_no_context_text,
            semantic_score=semantic_score if semantic_score <= 100 else 100,
            keyword_score=keyword_score if keyword_score <= 100 else 100,
            rerank_score=rerank_score if rerank_score <= 100 else 100,
            relevance_score=relevance_score if question_relevance_score != 0 else 0, 
            hallucination_index_by_equation=hallucination_index_by_equation if hallucination_index_by_equation < 100 else 100,
            hallucination_index_by_ml=hallucination_index_by_ml if hallucination_index_by_ml < 100 else 100,
            ars_lower_range=best_distance_a,
            ars_upper_range=worst_distance_a,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            model_type=model_type, 
            question=question
        )
        # add embeddings to answer
        if not no_context:
            add_embeddings_to_qna(answer_text, 'answer', embedding_model)
            hallucination_index_by_equation_final = 0
            if hallucination_index_by_equation < 0:
                hallucination_index_by_equation_final = 0
            elif hallucination_index_by_equation > 100:
                hallucination_index_by_equation_final = 100
            else:
                hallucination_index_by_equation_final = hallucination_index_by_equation
            return Response({
                'saved':True, 
                'mean_distance_a': mean_distance_a,
                'relevance_score': relevance_score if question_relevance_score != 0 else 0,
                'semantic_score': semantic_score,
                'keyword_score': keyword_score,
                'hallucination_index_by_equation': hallucination_index_by_equation_final,
                'hallucination_index_by_ml': hallucination_index_by_ml,
                'sources': new_sources_json,
            }, content_type="application/json")
        else:
            return Response({'saved':True, 'relevance_score': relevance_score}, content_type="application/json")

@api_view(['POST'])
def feedback_for_answers(request):
    if request.method == 'POST':
        json_request = JSONParser().parse(request)
        answer_text = json_request['answer_text']
        rating = json_request['rating']
        user_comment = json_request['user_comment'] if 'user_comment' in json_request else ''
        answer = Answer.objects.get(answer_text=answer_text)
        answer.rating = rating
        answer.user_comment = user_comment
        answer.save()
        return Response({'saved':True}, content_type="application/json")
    
@api_view(['GET'])
def delete_dataset(request):
    if request.method == 'GET':
        dataset_name = request.GET.get('dataset')
        user_email = request.GET.get('user_email')
        try:
            dataset_name = validate_dataset_name(dataset_name)
        except ValueError:
            return Response({'error':True, 'error_message': 'Invalid dataset name'}, status=400, content_type="application/json")
        dataset = Dataset.objects.get(dataset_name=dataset_name, user_email=user_email)
        papers = Papers.objects.filter(paper_dataset=dataset)
        for paper in papers:
            paper.delete()
        dataset.delete()

        # delete from chroma
        client = chromadb.PersistentClient(path='/code/chroma_storage/.')
        client.delete_collection(name=dataset_name)

        # delete the pdf folder
        pdf_folder = safe_path('data/pdfs', dataset_name)
        #  delete /data/data_chunks/ + dataset_name + .txt
        data_chunks_file = safe_path('data/data_chunks', dataset_name + '.txt')
        if os.path.exists(data_chunks_file):
            try:
                os.remove(data_chunks_file)
            except:
                return Response({'error':True, 'error_message': 'Could not delete data chunks file'}, content_type="application/json")
            
        # delete files from media folder
        media_folder = safe_path('media/papers', dataset_name)
        if os.path.exists(media_folder):
            # remove all files with output_file name in thier name
            files = [f for f in os.listdir(media_folder) if dataset_name in f]
            # remove all files with output_file name in thier name
            for f in files:
                media_file = safe_path(media_folder, f)
                if f.endswith('.pdf') and os.path.exists(media_file):
                    try:
                        os.remove(media_file)
                    except:
                        return Response({'error':True, 'error_message': 'Could not delete media folder'}, content_type="application/json")

        if os.path.exists(pdf_folder):
            # remove all files with output_file name in thier name
            # files = [f for f in os.listdir(pdf_folder) if dataset_name in f]
            # remove all files with output_file name in thier name
            try:
                shutil.rmtree(pdf_folder)
            except:
                return Response({'error':True, 'error_message': 'Could not delete pdf folder'}, content_type="application/json")
        return Response({'deleted':True}, content_type="application/json")
    

@api_view(['POST'])
def add_ollama_models(request):
    if request.method == 'POST':
        json_request = JSONParser().parse(request)
        ollama_models = json_request['llms']
        for ollama_model in ollama_models:
            if Model.objects.filter(model_name=ollama_model['name']).count() == 0:
                Model.objects.create(
                    model_name=ollama_model['name'],
                    model_size=ollama_model['size']
                )
        return Response({'added':True}, content_type="application/json")
    
@api_view(['POST'])
def add_embedding_models(request):
    if request.method == 'POST':
        json_request = JSONParser().parse(request)
        embedding_models = json_request['embedding_models']
        for embedding_model in embedding_models:
            if EmbeddingModel.objects.filter(model_name=embedding_model['name']).count() == 0:
                EmbeddingModel.objects.create(
                    model_name=embedding_model['name'],
                    model_size=embedding_model['size'],
                    model_source=embedding_model['source'],
                )
                get_embedding_model_ef(embedding_model['name'], True)
        return Response({'added':True}, content_type="application/json")
    
@api_view(['GET'])
def get_frontend_settings(request):
    if request.method == 'GET':
        # check if settings exist
        if FrontEndSettings.objects.count() == 0:
            # create default settings
            FrontEndSettings.objects.create(
                show_no_context_switch=False,
                azure_login=False,
                django_login=False,
                restriction_without_login=False,
                disable_chat_without_login=False,
                saved_date_time=make_aware(datetime.datetime.now())
            )
        
        # get the latest settings
        frontend_settings = FrontEndSettings.objects.latest('saved_date_time')
        frontend_settings_obj = {
            'show_no_context_switch': frontend_settings.show_no_context_switch,
            'restriction_without_login': frontend_settings.restriction_without_login,
            'azure_login': frontend_settings.azure_login,
            'django_login': frontend_settings.django_login,
            'disable_chat_without_login': frontend_settings.disable_chat_without_login
        }
        return Response({'settings':frontend_settings_obj})
    
@api_view(['GET'])
def add_demo_dataset_api(request):
    if request.method == 'GET':
        embedding_model = request.GET.get('embedding_model', 'nomic-embed-text:latest')
        add_demo_dataset(embedding_model)
        return Response({'added':True}, content_type="application/json")

    
@api_view(['GET'])
def get_vector_embeddings(request):
    if request.method == 'GET':
        datasets_param = request.GET.get('datasets')
        question_id_param = request.GET.get('question_id')

        # Validate datasets input
        if not datasets_param or not re.match(r'^[a-zA-Z0-9_,\-]+$', datasets_param):
            return Response({'error': True, 'error_message': 'Invalid datasets parameter'}, status=400)

        datasets = datasets_param.split(',')

        # Validate question_id input
        if question_id_param:
            if not question_id_param.isdigit():
                return Response({'error': True, 'error_message': 'Invalid question_id parameter'}, status=400)

            question_id = int(question_id_param)
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                return Response({'error': True, 'error_message': 'Question not found'}, status=404)

            if question.pca_x == 0 and question.pca_y == 0 and question.pca_z == 0:
                add_pca_to_qna_and_dataset(question_id)

            # return Response({'success': True}, status=200)

        pca_embeddings = []
        for dataset_name in datasets:
            dataset = Dataset.objects.get(dataset_name=dataset_name)
            chunks_objects = chunks.objects.filter(chunk_dataset=dataset)
            for chunk in chunks_objects:
                pca_embeddings.append({
                    'pca_x': chunk.pca_x,
                    'pca_y': chunk.pca_y,
                    'pca_z': chunk.pca_z,
                    'dataset': chunk.chunk_dataset.dataset_name
                })

        if question_id:
            question = Question.objects.get(id=question_id)
            pca_embeddings.append({
                'pca_x': question.pca_x,
                'pca_y': question.pca_y,
                'pca_z': question.pca_z,
                'dataset': 'question'
            })
            answer = Answer.objects.filter(question=question)[0]
            pca_embeddings.append({
                'pca_x': answer.pca_x,
                'pca_y': answer.pca_y,
                'pca_z': answer.pca_z,
                'dataset': 'answer'
            })
            sources = Source.objects.filter(question=question)
            for source in sources:
                chunk = chunks.objects.get(id=source.chunk.id)
                pca_embeddings.append({
                    'pca_x': chunk.pca_x,
                    'pca_y': chunk.pca_y,
                    'pca_z': chunk.pca_z,
                    'dataset': 'source'
                })
        return Response({'pca_embeddings': pca_embeddings})
    
@api_view(['GET'])
def add_dataset_embeddings(request):
    if request.method == 'GET':
        dataset_name_request = request.GET.get('dataset')
        # add validation for dataset name
        if not dataset_name_request or not re.match(r'^[a-zA-Z0-9_\-]+$', dataset_name_request):
            return Response({'error': True, 'error_message': 'Invalid dataset name'}, status=400)
        else:
            dataset_name = dataset_name_request
            add_embeddings_to_qna(dataset_name)
            add_pca_to_qna_and_dataset(dataset_name)
            return Response({'added':True}, content_type="application/json")
    
@api_view(['POST'])
def get_distance_between_answers(request):
    if request.method == 'POST':
        json_request = JSONParser().parse(request)
        sentence1 = json_request['sentence1']
        sentence2 = json_request['sentence2']
        embedding_model = json_request['embedding_model']
        distances = get_answer_distance(sentence1, sentence2, embedding_model)
        return Response({'distances': distances}, content_type="application/json")
    
@api_view(['GET'])
def get_embedding_model_details(request):
    if request.method == 'GET':
        dataset = request.GET.get('dataset')
        embedding_model_name = Dataset.objects.get(dataset_name=dataset).embedding_model
        embedding_model = EmbeddingModel.objects.get(model_name=embedding_model_name)
        embedding_model_obj = {
            'model_name': embedding_model.model_name,
            'model_size': embedding_model.model_size,
            'model_source': embedding_model.model_source,
            'best_distance_q': embedding_model.best_distance_q,
            'worst_distance_q': embedding_model.worst_distance_q,
            'best_distance_ac': embedding_model.best_distance_ac,
            'worst_distance_ac': embedding_model.worst_distance_ac,
            'best_distance_nac': embedding_model.best_distance_nac,
            'worst_distance_nac': embedding_model.worst_distance_nac,
        }
        return Response({'embedding_model': embedding_model_obj})
    
@api_view(['POST'])
def get_dataset_sections(request):
    if request.method == 'POST':
        json_request = JSONParser().parse(request)
        dataset_name = json_request['dataset_name']
        dataset = Dataset.objects.get(dataset_name=dataset_name)
        # order by count descending and then by alphanumeric order
        sections = PaperSections.objects.filter(section_dataset=dataset).order_by('-section_count', 'section_title')
        sections_json = []
        for section in sections:
            sections_json.append({
                'section_title': section.section_title,
                'section_count': section.section_count
            })
        return Response({'sections': sections_json}, content_type="application/json")
    
# get username if access token is valid
@api_view(['POST'])
def get_username(request):
    if request.method == 'POST':
        access_token = request.data['access_token']

        try:
            token = AccessToken(access_token)
            user_id = token.payload['user_id']
            user = User.objects.get(id=user_id).username
            user_email = User.objects.get(id=user_id).email
            user_group = User.objects.get(id=user_id).groups.all()[0].name if User.objects.get(id=user_id).groups.count() else ''
            return Response({'username': user, 'user_email': user_email, 'user_group': user_group}, content_type="application/json")
        except:
            return Response({'username': ''}, content_type="application/json")
        
@api_view(['POST'])
def disclaimer_agreement(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.data['username'])
        DisclaimerAgreement.objects.create(
            user=user,
            agreement_date_time=make_aware(datetime.datetime.now())
        )
        return Response({'agreed':True}, content_type="application/json")


@api_view(['GET'])
@permission_classes([AllowAny])
def secure_media(request, file_path):
    django_login_enabled = False
    if FrontEndSettings.objects.exists():
        frontend_settings = FrontEndSettings.objects.latest('saved_date_time')
        django_login_enabled = frontend_settings.django_login

    normalized_path = file_path.replace('\\', '/')
    is_public_library_media = False
    if normalized_path.startswith('papers/'):
        path_parts = normalized_path.split('/')
        if len(path_parts) > 1 and path_parts[1]:
            dataset_name = path_parts[1]
            is_public_library_media = Dataset.objects.filter(
                dataset_name=dataset_name,
                user_email='-'
            ).exists()

    is_authenticated_user = bool(getattr(request, 'user', None) and request.user.is_authenticated)
    auth_header = request.headers.get('Authorization', '')
    bearer_token = auth_header.split(' ', 1)[1] if auth_header.startswith('Bearer ') and ' ' in auth_header else ''
    static_tokens = [
        os.environ.get('AUTH_TOKEN_PROD'),
        os.environ.get('AUTH_TOKEN_DEV'),
        os.environ.get('VITE_AUTH_TOKEN_PROD'),
        os.environ.get('VITE_AUTH_TOKEN_DEV'),
    ]
    valid_static_tokens = [token for token in static_tokens if token]
    has_valid_static_token = (
        auth_header in valid_static_tokens
        or bearer_token in valid_static_tokens
        or any(auth_header == f'Bearer {token}' for token in valid_static_tokens)
    )

    if django_login_enabled and not is_public_library_media and not is_authenticated_user and not has_valid_static_token:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        absolute_path = safe_join(settings.MEDIA_ROOT, file_path)
    except ValueError:
        raise Http404('File not found')

    if not os.path.exists(absolute_path) or not os.path.isfile(absolute_path):
        raise Http404('File not found')

    return FileResponse(open(absolute_path, 'rb'))

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def ollama_generate(request):
    if request.method == 'POST':
        try:
            json_request = JSONParser().parse(request)
            model = json_request['model']
            prompt = json_request['prompt']
            system = json_request.get('system', '')
            stream = json_request.get('stream', True)
            think = json_request.get('think', True)
            temperature = json_request.get('options', {}).get('temperature', 0.7)
            top_k = json_request.get('options', {}).get('top_k', 50)
            top_p = json_request.get('options', {}).get('top_p', 0.9)

            # Validate model_name input
            if not model or not re.match(r'^[a-zA-Z0-9_\-:.]+$', model):
                return Response({'error': True, 'error_message': 'Invalid model name'}, content_type="application/json")

            client = OllamaClient(
                host = os.environ.get('OLLAMA_SERVER')
            )
            
            # Non-streaming path: stream=False
            if not stream:
                try:
                    options = {'temperature': temperature, 'top_k': top_k, 'top_p': top_p}
                    try:
                        # Call without streaming - returns a single dict object
                        response = client.generate(
                            model=model,
                            prompt=prompt,
                            system=system,
                            stream=False,
                            think=think,
                            options=options,
                        )
                    except Exception as e:
                        # Some models do not support think mode; retry once without think.
                        if think and ('does not support think' in str(e).lower() or 'unknown field "think"' in str(e).lower()):
                            response = client.generate(
                                model=model,
                                prompt=prompt,
                                system=system,
                                stream=False,
                                options=options,
                            )
                        else:
                            raise
                    
                    # Extract response and thinking from the single object
                    return Response({
                        'response': response.get('response', ''),
                        'thinking': response.get('thinking', '')
                    }, content_type="application/json")
                except Exception:
                    logger.exception("Ollama generate request failed")
                    return Response({'error': True, 'error_message': 'Model generation failed'}, status=500, content_type="application/json")
            
            # Streaming path: stream=True
            def stream_response():
                try:
                    options = {'temperature': temperature, 'top_k': top_k, 'top_p': top_p}
                    try:
                        # Use named args to avoid accidentally passing `system` as `suffix` (insert mode).
                        response = client.generate(
                            model=model,
                            prompt=prompt,
                            system=system,
                            stream=stream,
                            think=think,
                            options=options,
                        )
                    except Exception as e:
                        # Some models do not support think mode; retry once without think.
                        if think and ('does not support think' in str(e).lower() or 'unknown field "think"' in str(e).lower()):
                            response = client.generate(
                                model=model,
                                prompt=prompt,
                                system=system,
                                stream=stream,
                                options=options,
                            )
                        else:
                            raise
                    for part in response:
                        # Stream thinking if present
                        if 'thinking' in part and part['thinking']:
                            yield json.dumps({'type': 'thinking', 'content': part['thinking'], 'done': False}) + '\n'
                        
                        # Stream response if present
                        if 'response' in part and part['response']:
                            yield json.dumps({'type': 'response', 'content': part['response'], 'done': False}) + '\n'
                    
                    # Signal completion
                    yield json.dumps({'type': 'done', 'content': '', 'done': True}) + '\n'
                except Exception:
                    logger.exception("Streaming Ollama generate request failed")
                    yield json.dumps({'error': True, 'error_message': 'Model generation failed', 'done': True}) + '\n'
            
            return StreamingHttpResponse(
                stream_response(),
                content_type='application/x-ndjson'
            )
        except Exception:
            logger.exception("Invalid Ollama generate request")
            return Response({'error': True, 'error_message': 'Unable to process generation request'}, status=500, content_type="application/json")
        
@api_view(['POST'])
def ollama_chat(request):
    if request.method == 'POST':
        try:
            json_request = JSONParser().parse(request)
            new_conversation = json_request['new_conversation']
            model = json_request['model']
            messages = json_request['messages']
            stream = json_request.get('stream', True)
            think = json_request.get('think', False)
            temperature = json_request.get('options', {}).get('temperature', 0.7)
            top_k = json_request.get('options', {}).get('top_k', 50)
            top_p = json_request.get('options', {}).get('top_p', 0.9)
            tools = json_request.get('tools', [])

            # Validate model_name input
            if not model or not re.match(r'^[a-zA-Z0-9_\-:.]+$', model):
                return Response({'error': True, 'error_message': 'Invalid model name'}, content_type="application/json")

            client = OllamaClient(
                host = os.environ.get('OLLAMA_SERVER')
            )

            # save the question to the database with the model name and messages
            dataset_name = model + '_direct_chat'
            if not Dataset.objects.filter(dataset_name=dataset_name).exists():
                Dataset.objects.create(
                    dataset_name=dataset_name,
                    library_type='papers',
                    dataset_size=0,
                    user = '-',
                    user_email = '-',
                    user_group = '-',
                    dataset_date_time=make_aware(datetime.datetime.now()),
                    embedding_model = '',
                )
            dataset = Dataset.objects.get(dataset_name=dataset_name)
            
            # Ensure model exists in database before creating questions
            model_type, _ = Model.objects.get_or_create(model_name=model, defaults={'model_size': '0'})
            
            if new_conversation:
                conversation = Conversation.objects.create(
                    question_answer_count=1,
                    conversation_dataset=Dataset.objects.get(dataset_name=dataset_name),
                    start_date_time=make_aware(datetime.datetime.now())
                )
                Question.objects.create(
                    question_text=messages[-1]['content'] if messages else '',
                    conversation=conversation,
                    question_dataset=dataset,
                    model_type=model_type,
                )
            else:
                conversation = Conversation.objects.filter(conversation_dataset=dataset).order_by('-start_date_time').first()
                if conversation:
                    Question.objects.create(
                        question_text=messages[-1]['content'] if messages else '',
                        conversation=conversation,
                        question_dataset=dataset,
                        model_type=model_type,
                    )
                else:
                    conversation = Conversation.objects.create(
                        question_answer_count=1,
                        conversation_dataset=dataset,
                        start_date_time=make_aware(datetime.datetime.now())
                    )
                    Question.objects.create(
                        question_text=messages[-1]['content'] if messages else '',
                        conversation=conversation,
                        question_dataset=dataset,
                        model_type=model_type,
                    )

            # Non-streaming path: stream=False
            if not stream:
                try:
                    options = {'temperature': temperature, 'top_k': top_k, 'top_p': top_p}
                    response = client.chat(
                        model=model,
                        messages=messages,
                        stream=False,
                        think=think,
                        options=options,
                        tools=tools
                    )

                    # Extract message content, thinking, and tool calls from the single object
                    message = response.get('message', {}) if isinstance(response, dict) else getattr(response, 'message', {})
                    response_content = message.get('content', '') if isinstance(message, dict) else getattr(message, 'content', '')
                    response_thinking = message.get('thinking', '') if isinstance(message, dict) else getattr(message, 'thinking', '')
                    tool_calls = message.get('tool_calls', []) if isinstance(message, dict) else getattr(message, 'tool_calls', [])
                    return_response = {
                        'content': response_content,
                        'thinking': response_thinking,
                        'tool_calls': tool_calls if tool_calls else [],
                    }
                    
                    return Response(return_response, content_type="application/json")
                except Exception:
                    logger.exception("Ollama chat request failed")
                    return Response({'error': True, 'error_message': 'Model chat failed'}, status=500, content_type="application/json")
            
            # Streaming path: stream=True
            def stream_response():
                try:
                    options = {'temperature': temperature, 'top_k': top_k, 'top_p': top_p}
                    response = client.chat(
                        model=model,
                        messages=messages,
                        stream=stream,
                        think=think,
                        options=options,
                        tools=tools
                    )
                    for part in response:
                        message = part.get('message', {})
                        # Stream thinking if present (part['message']['thinking'])
                        thinking = message.get('thinking', '')
                        if thinking:
                            yield json.dumps({'type': 'thinking', 'content': thinking, 'done': False}) + '\n'
                        
                        # Stream response content (part['message']['content'])
                        content = message.get('content', '')
                        if content:
                            yield json.dumps({'type': 'response', 'content': content, 'done': False}) + '\n'
                    
                    # Signal completion
                    yield json.dumps({'type': 'done', 'content': '', 'done': True}) + '\n'
                except Exception:
                    logger.exception("Streaming Ollama chat request failed")
                    yield json.dumps({'error': True, 'error_message': 'Model chat failed', 'done': True}) + '\n'
            
            return StreamingHttpResponse(
                stream_response(),
                content_type='application/x-ndjson'
            )
        except Exception:
            logger.exception("Invalid Ollama chat request")
            return Response({'error': True, 'error_message': 'Unable to process chat request'}, status=500, content_type="application/json")
        
@api_view(['POST'])
def get_ollama_models(request):
    if request.method == 'POST':
        models = []
        try:
            client = OllamaClient(host=os.environ.get('OLLAMA_SERVER'))
            
            response: ListResponse = client.list()
            for model in response.models:
                if model.size is not None and model.size > 0:
                    if model.details:
                        quantization_level = model.details.get('quantization_level', 'unknown')
                        if quantization_level != 'F16' and not Model.objects.filter(model_name=model.model).exists():
                            Model.objects.create(
                                model_name=model.model,
                                model_size=f"{(model.size * 1e-9):.2f}",
                            )
                        models.append({
                            'name': model.model,
                            'size': model.size,
                            'family': model.details.get('family', 'unknown'),
                            'format': model.details.get('format', 'unknown'),
                            'parameter_size': model.details.get('parameter_size', 'unknown'),
                            'quantization_level': quantization_level,
                        })
            return Response({'added':True, 'models': models}, content_type="application/json")
        except Exception:
            logger.exception("Unable to list Ollama models")
            return Response({'error': True, 'error_message': 'Unable to list models'}, status=500, content_type="application/json")
        
@api_view(['POST'])
def ollama_pull_model(request):
    if request.method == 'POST':
        json_request = JSONParser().parse(request)
        model_name = json_request.get('name', '')

        # Validate model_name input
        if not model_name or not re.match(r'^[a-zA-Z0-9_\-:.]+$', model_name):
            return Response({'error': True, 'error_message': 'Invalid model name'}, content_type="application/json")
        try:
            client = OllamaClient(host=os.environ.get('OLLAMA_SERVER'))
            
            def stream_response():
                try:
                    current_digest = ''
                    bars = {}
                    response = client.pull(model=model_name, stream=True)
                    for part in response:
                        digest = part.get('digest', '')
                        status_txt = part.get('status', '')

                        if digest != current_digest and current_digest in bars:
                            yield json.dumps({
                                'type': 'layer_complete',
                                'digest': current_digest,
                                'status': 'layer completed',
                                'done': False,
                            }) + '\n'

                        if not digest:
                            yield json.dumps({
                                'type': 'status',
                                'status': status_txt,
                                'done': False,
                            }) + '\n'
                            current_digest = digest
                            continue

                        total = part.get('total', 0)
                        if digest not in bars and total:
                            bars[digest] = {
                                'total': total,
                                'completed': 0,
                            }

                        completed = part.get('completed')
                        if digest in bars and completed is not None:
                            previous_completed = bars[digest]['completed']
                            delta = completed - previous_completed
                            if delta < 0:
                                delta = 0
                            bars[digest]['completed'] = completed
                            layer_total = bars[digest]['total']
                            percent = round((completed / layer_total) * 100, 2) if layer_total else 0
                            yield json.dumps({
                                'type': 'progress',
                                'status': status_txt,
                                'digest': digest,
                                'total': layer_total,
                                'completed': completed,
                                'delta': delta,
                                'percent': percent,
                                'done': False,
                            }) + '\n'
                        else:
                            yield json.dumps({
                                'type': 'status',
                                'status': status_txt,
                                'digest': digest,
                                'done': False,
                            }) + '\n'

                        current_digest = digest
                    
                    # Signal completion
                    yield json.dumps({'status': 'completed', 'progress': 100, 'done': True}) + '\n'
                except Exception:
                    logger.exception("Streaming Ollama model pull failed")
                    yield json.dumps({'error': True, 'error_message': 'Model download failed', 'done': True}) + '\n'
            
            return StreamingHttpResponse(
                stream_response(),
                content_type='application/x-ndjson'
            )
        except Exception:
            logger.exception("Unable to start Ollama model pull")
            return Response({'error': True, 'error_message': 'Unable to start model download'}, status=500, content_type="application/json")