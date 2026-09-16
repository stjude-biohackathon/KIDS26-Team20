from django.contrib import admin
from .models import Model, EmbeddingModel, RerankerModel, Dataset, Papers, Videos, chunks, Conversation, Question, Answer, Source, FrontEndSettings, DisclaimerAgreement, PaperSections

class ModelAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'model_size']

class EmbeddingModelAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'model_size', 'model_source', 'best_distance_q', 'worst_distance_q']

class RerankerModelAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'cutoff_score']

class DatasetAdmin(admin.ModelAdmin):
    list_display = ['dataset_name', 'zotero_id', 'dataset_size', 'chunksize', 'overlap', 'user', 'user_email', 'user_group', 'embedding_model', 'embedding_added', 'reranker', 'direct_chat_without_docs', 'dataset_date_time']

class PapersAdmin(admin.ModelAdmin):
    list_display = ['paper_title', 'paper_attachment', 'highlighted_attachment', 'paper_dataset', 'paper_date_time']

class PaperSectionsAdmin(admin.ModelAdmin):
    list_display = ['section_title', 'section_count', 'section_dataset']

class VideosAdmin(admin.ModelAdmin):
    list_display = ['video_title', 'video_link', 'video_dataset', 'video_date_time']

class chunksAdmin(admin.ModelAdmin):
    list_display = ['chunk_text', 'pca_x', 'pca_y', 'pca_z', 'chunk_dataset', 'chunk_paper', 'chunk_date_time']

class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_answer_count', 'start_date_time', 'last_date_time', 'conversation_dataset', 'user']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_dataset', 'relevance_score' ,'conversation', 'saved_date_time']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_text', 'model_type', 'relevance_score', 'hallucination_index_by_equation', 'hallucination_index_by_ml', 'question', 'saved_date_time']

class SourceAdmin(admin.ModelAdmin):
    list_display = ['source_doc', 'source_pointer', 'vector_score', 'bm25_score', 'rank', 'context', 'question']

class FrontEndSettingsAdmin(admin.ModelAdmin):
    list_display = ['show_no_context_switch', 'azure_login', 'django_login', 'restriction_without_login', 'saved_date_time']

class DisclaimerAgreementAdmin(admin.ModelAdmin):
    list_display = ['user', 'agreement_date_time']

admin.site.register(Model, ModelAdmin)
admin.site.register(EmbeddingModel, EmbeddingModelAdmin)
admin.site.register(RerankerModel, RerankerModelAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Papers, PapersAdmin)
admin.site.register(PaperSections, PaperSectionsAdmin)
admin.site.register(Videos, VideosAdmin)
admin.site.register(chunks, chunksAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(FrontEndSettings, FrontEndSettingsAdmin)
admin.site.register(DisclaimerAgreement, DisclaimerAgreementAdmin)