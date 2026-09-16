from django.urls import include, path
from rest_framework import routers
from .views import apis, homepage, mygpt_viewsets, LogoutView

router = routers.DefaultRouter()
router.register(r'llms', mygpt_viewsets.ModelViewSet)
router.register(r'embedding_models', mygpt_viewsets.EmbeddingModelViewSet)
router.register(r'papers', mygpt_viewsets.PapersViewSet)
router.register(r'questions', mygpt_viewsets.QuestionsViewSet)
router.register(r'answers', mygpt_viewsets.AnswersViewSet)
router.register(r'disclaimer_agreements', mygpt_viewsets.DisclaimerAgreementViewSet)

urlpatterns = [
    path('', homepage.home, name='home'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	path('api/get_datasets/', apis.get_datasets, name='get_datasets'),
    path('api/get_dataset_details/', apis.get_dataset_details, name='get_dataset_details'),
	path('api/update_dataset/', apis.update_dataset, name='update_dataset'),
    path('api/get_documents/', apis.get_documents, name='get_documents'),
	path('api/get_sections/', apis.get_dataset_sections, name='get_sections'),
	path('api/get_context/', apis.get_context, name='get_context'),
	path('api/get_conversation_history/', apis.get_conversations_by_dataset, name='conversation_history'),
	path('api/get_question_details/', apis.get_question_details, name='get_question_details'),
	path('api/get_embedding_model_details/', apis.get_embedding_model_details, name='get_embedding_model_details'),
	path('api/save_answer/', apis.save_answer, name='save_answer'),
	path('api/feedback/', apis.feedback_for_answers, name='feedback'),
	path('api/delete_dataset/', apis.delete_dataset, name='delete_dataset'),
	path('api/add_ollama_models/', apis.add_ollama_models, name='add_ollama_models'),
	path('api/add_embedding_models/', apis.add_embedding_models, name='add_embedding_models'),
	path('api/frontend_settings/', apis.get_frontend_settings, name='frontend_settings'),
	path('api/add_demo_library/', apis.add_demo_dataset_api, name='add_demo_dataset'),
	path('api/get_vector_embeddings/', apis.get_vector_embeddings, name='get_vector_embeddings'),
	path('api/add_dataset_embeddings/', apis.add_dataset_embeddings, name='add_dataset_embeddings'),
	path('api/get_distance_between_answers/', apis.get_distance_between_answers, name='get_distance_between_answers'),
	path('api/get_username/', apis.get_username, name='get_username'),
	path('api/submit_disclaimer_agreement/', apis.disclaimer_agreement, name='disclaimer_agreement'),
    path('api/ollama_generate/', apis.ollama_generate, name='ollama_generate'),
    path('api/ollama_chat/', apis.ollama_chat, name='ollama_chat'),
    path('api/get_ollama_models/', apis.get_ollama_models, name='get_ollama_models'),
    path('api/ollama_pull_model/', apis.ollama_pull_model, name='ollama_pull_model'),
	path('logout/', LogoutView.as_view(), name='logout'),
]