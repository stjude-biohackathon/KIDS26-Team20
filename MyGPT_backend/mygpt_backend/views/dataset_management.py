"""
Dataset management functions
"""
import datetime
from django.core.files.base import File
from django.utils.timezone import make_aware
from tqdm import tqdm
import chromadb

from ..models import Papers, Dataset, Question, Answer, Conversation
from .embedding_utils import get_embedding_model_ef
from .analytics import add_pca_to_chunks


def add_demo_dataset(embedding_model_request='nomic-embed-text:latest'):
    """Add Turing Way dataset"""
    documents_directory = '/code/data'
    documents = []
    metadatas = []
    dataset_name = 'Turing_Way'

    if Dataset.objects.filter(dataset_name=dataset_name).exists():
        return dataset_name

    titles = []
    client = chromadb.PersistentClient(path='/code/chroma_storage/.')

    embedding_model_ef = get_embedding_model_ef(embedding_model_request)

    # Rebuild a stale collection when the corresponding database row is missing.
    if len(client.list_collections()):
        for collection in client.list_collections():
            if collection.name == dataset_name:
                client.delete_collection(name=dataset_name)
    collection = client.get_or_create_collection(name=dataset_name, embedding_function=embedding_model_ef)

    # Create ids from the current count
    count = collection.count()
    print(f'Collection already contains {count} documents')

    # Load the documents in batches of 100
    if count == 0:
        with open(f'{documents_directory}/data_chunks/Turing_Way.txt', 'r') as file:
            for line_number, line in enumerate(
                tqdm((file.readlines()), desc=f'Reading Turing_Way.txt'), 1
            ):
                # Strip whitespace and append the line to the documents list
                line = line.strip()
                #convert line to json
                line_json = eval(line)
                documents.append(line_json['content'])
                metadatas.append({'filename': line_json['title'], 'page': line_json['page'], 'type': line_json['type']})
                if line_json['title'] not in titles:
                    titles.append(line_json['title'])
        ids = [str(i) for i in range(count, count + len(documents))]
       
        for i in tqdm(
            range(0, len(documents), 100), desc='Adding documents', unit_scale=100
        ):  
            try:
                collection.add(
                    ids=ids[i : i + 100],
                    documents=documents[i : i + 100],
                    metadatas=metadatas[i : i + 100],  # type: ignore
                )
            except:
                print('error adding documents')

        new_count = 0
        try:
            new_count = collection.count()
        except:
            print('error counting documents')
        
        print(f'new_count: {new_count}')
        dataset = Dataset.objects.create(
            dataset_name=dataset_name,
            library_type='papers',
            dataset_size=new_count,
            embedding_model=embedding_model_request,
            chunksize=1000,
            chunking_method='fixed_chunk_size',
            overlap=True,
            use_bm25=True,
            distance_function='l2',
            use_reranker=True,
            reranker='qnli-electra-base (default)',
            dataset_date_time=make_aware(datetime.datetime.now()),
            user='-',
            user_email='-',
            user_group='user',
            documents_language='english',
            dataset_prompt='###INSTRUCTIONS#### \nUse following information to answer the question in less than 200 words, try not to use any other information other than provided context. if the information is not in the context, then tell user that information is not found in the documents.\n ### CONTEXT ####'
        )

        for (idx, title) in enumerate(titles):
            paper = Papers.objects.create(
                paper_title=title,
                paper_dataset=dataset,
                paper_date_time=make_aware(datetime.datetime.now())
            )
            with open(f'{documents_directory}/pdfs/{dataset_name}/paper{idx+1}.pdf', 'rb') as f:
                paper.paper_attachment.save(dataset_name + '/paper' + str(idx+1) + '.pdf', File(f), save=True)

        # add pca to chunks
        add_pca_to_chunks()
           
        print(f'Added {new_count - count} documents')

    return dataset_name

def get_conversation_json(question_text):
    """Get conversation history as JSON"""
    conversation_id = Question.objects.filter(question_text=question_text)[0].conversation.id
    conversation = Conversation.objects.get(id=conversation_id)
    questions = Question.objects.filter(conversation=conversation).order_by('saved_date_time')
    conversation_json = []
    for question in questions:
        answers = Answer.objects.filter(question=question)
        qna_json = {
            'question': question.question_text,
            'answers': answers[0].answer_text,
        }
        conversation_json.append(qna_json)
    return conversation_json


def get_previous_qna_json(question_text):
    """Get previous Q&A as JSON"""
    question = Question.objects.filter(question_text=question_text)[0]
    answers = Answer.objects.filter(question=question)
    conversation_json = []
    qna_json = {
        'question': question.question_text,
        'answers': answers[0].answer_text,
    }
    conversation_json.append(qna_json)
    return conversation_json