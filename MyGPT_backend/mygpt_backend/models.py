from django.db import models
from django.utils import timezone
import os
from django.conf import settings

model_types = (
	('chatGPT', 'chatGPT'),
	('AI21', 'AI21'),
	('BioGPT', 'BioGPT'),
	('BioGPT-ft', 'BioGPT-ft'),
	('Llama3', 'Llama3'),
	('Llama2', 'Llama2'),
	('Llama2-ft', 'Llama2-ft'),
	('-', '-')
)

rating_types = (
	(1, 'correct'),
	(0, 'n/a'),
	(-1, 'incorrect'),
)

question_types = (
	('keyword', 'keyword'),
	('yesno', 'yesno'),
	('data_query', 'data_query'),
	('summarize', 'summarize'),
	('complex', 'complex'),
	('other', 'other'),
)

embedding_model_source = (
	('ollama', 'ollama'),
	('sentence-transformer', 'sentence-transformer'),
	('huggingface', 'huggingface'),
)

chunking_methods_choice = (
	('fixed_chunk_size', 'fixed_chunk_size'),
	('structure_preserving', 'structure_preserving'),
	('-', '-')
)

document_languages = (
	('english', 'english'),
	('french', 'french'),
	('spanish', 'spanish'),
	('portuguese', 'portuguese'),
	('german', 'german'),
	('italian', 'italian'),
	('dutch', 'dutch'),
	('arabic', 'arabic'),
	('hindi', 'hindi'),
	('hungarian', 'hungarian'),
	('unknown', 'unknown'),
)

class Dataset(models.Model):
	dataset_name = models.CharField(max_length=200, default='-')
	library_type = models.CharField(max_length=20, default='papers')
	zotero_id = models.CharField(max_length=40, default='-')
	dataset_size = models.IntegerField(default=0)
	user = models.CharField(max_length=200, default='-')
	user_email = models.CharField(max_length=200, default='-')
	user_group = models.CharField(max_length=200, default='-')
	embedding_added = models.BooleanField(default=False)
	embedding_model = models.CharField(max_length=60, default='-')
	chunking_method = models.CharField(max_length=40, choices=chunking_methods_choice, default='-')
	chunksize = models.IntegerField(default=1000)
	overlap = models.BooleanField(default=False)
	use_bm25 = models.BooleanField(default=False)
	use_reranker = models.BooleanField(default=False)
	reranker = models.CharField(max_length=100, default='-')
	documents_language = models.CharField(max_length=40, choices=document_languages, default='-')
	distance_function = models.CharField(max_length=40, default='l2')
	coefficient_a_Qsem = models.FloatField(default=4)
	coefficient_b_Qkey = models.FloatField(default=-4)
	coefficient_c_Qrank = models.FloatField(default=-1)
	coefficient_x_Asem = models.FloatField(default=5)
	coefficient_y_Akey = models.FloatField(default=-2)
	coefficient_z_Arank = models.FloatField(default=0)
	coefficient_p_QRS = models.FloatField(default=1)
	coefficient_q_ARS = models.FloatField(default=2)
	HI_by_equation = models.BooleanField(default=False)
	dataset_prompt = models.TextField(default='-')
	direct_chat_without_docs = models.BooleanField(default=False)
	dataset_date_time = models.DateTimeField(default=timezone.now, null=True)

	def __str__(self):
		return self.dataset_name
	
	def delete(self, *args, **kwargs):
		# empty the directory
		for root, dirs, files in os.walk(os.path.join(settings.MEDIA_ROOT, 'papers', str(self.dataset_name)), topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))
		# check if the director exists and delete it
		if os.path.exists(os.path.join(settings.MEDIA_ROOT, 'papers', str(self.dataset_name))):
			os.rmdir(os.path.join(settings.MEDIA_ROOT, 'papers', str(self.dataset_name)))
		super().delete(*args, **kwargs)

class Papers(models.Model):
	paper_title = models.TextField(default='-')
	paper_attachment = models.FileField(upload_to='papers', default='-')
	highlighted_attachment = models.FileField(upload_to='papers', default='-')
	paper_dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE)
	paper_date_time = models.DateTimeField(default=timezone.now, null=True)

	class Meta:
		verbose_name_plural = 'papers'
		verbose_name = 'paper'

	def __str__(self):
		return self.paper_title
	
class PaperSections(models.Model):
	section_title = models.TextField(default='-')
	section_count = models.IntegerField(default=0)
	section_dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'paper sections'
		verbose_name = 'paper section'

	def __str__(self):
		return self.section_title

class Videos(models.Model):
	video_title = models.TextField(default='-')
	video_link = models.TextField(default='-')
	video_dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE)
	video_date_time = models.DateTimeField(default=timezone.now, null=True)

	class Meta:
		verbose_name_plural = 'videos'
		verbose_name = 'video'

	def __str__(self):
		return self.video_title
	
class chunks(models.Model):
	chunk_text = models.TextField(default='-')
	embedding = models.TextField(default='-')
	pca_x = models.FloatField(default=0)
	pca_y = models.FloatField(default=0)
	pca_z = models.FloatField(default=0)
	chunk_dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
	chunk_paper = models.ForeignKey(Papers, on_delete=models.CASCADE, null=True)
	chunk_video = models.ForeignKey(Videos, on_delete=models.CASCADE, null=True)
	chunk_date_time = models.DateTimeField(default=timezone.now, null=True)

	class Meta:
		verbose_name_plural = 'chunks'
		verbose_name = 'chunk'

	def __str__(self):
		return (str(self.chunk_dataset) + '-' + str(self.id))
	
class Conversation(models.Model):
	conversation_dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE)
	question_answer_count = models.IntegerField(default=0)
	user = models.CharField(max_length=200, default='-')
	start_date_time = models.DateTimeField(default=timezone.now, null=True)
	last_date_time = models.DateTimeField(default=timezone.now, null=True)

	def __str__(self):
		return str(self.id)

class Question(models.Model):
	question_text = models.TextField(default='-')
	translated_question_text = models.TextField(default='-')
	semantic_score = models.FloatField(default=0)
	keyword_score = models.FloatField(default=0)
	rerank_score = models.FloatField(default=0)
	relevance_score = models.FloatField(default=0)
	model_type =  models.ForeignKey('Model', on_delete=models.SET_DEFAULT, default=2)
	question_type = models.CharField(max_length=40, choices=question_types, default='other')
	keywords = models.CharField(max_length=200, default='-')
	ground_truth = models.TextField(default='-')
	qrs_lower_range = models.FloatField(default=0)
	qrs_upper_range = models.FloatField(default=0)
	embedding = models.TextField(default='-')
	pca_x = models.FloatField(default=0)
	pca_y = models.FloatField(default=0)
	pca_z = models.FloatField(default=0)
	question_dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE)
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
	saved_date_time = models.DateTimeField(default=timezone.now, null=True)

class Answer(models.Model):
	answer_text = models.TextField(default='-')
	translated_answer_text = models.TextField(default='-')
	answer_no_context_text = models.TextField(default='-')
	model_type =  models.ForeignKey('Model', on_delete=models.SET_DEFAULT, default=2)
	temperature = models.FloatField(default=0.4)
	top_k = models.IntegerField(default=20)
	top_p = models.FloatField(default=0.7)
	semantic_score = models.FloatField(default=0)
	keyword_score = models.FloatField(default=0)
	rerank_score = models.FloatField(default=0)
	relevance_score = models.FloatField(default=0)
	hallucination_index_by_equation = models.FloatField(default=0)
	hallucination_index_by_ml = models.FloatField(default=0)
	rating = models.IntegerField(choices=rating_types, default=0)
	user_comment = models.TextField(default='-')
	ars_lower_range = models.FloatField(default=0)
	ars_upper_range = models.FloatField(default=0)
	a_hi = models.FloatField(default=1)
	b_hi = models.FloatField(default=0.33)
	c_hi = models.FloatField(default=0.66)
	embedding = models.TextField(default='-')
	pca_x = models.FloatField(default=0)
	pca_y = models.FloatField(default=0)
	pca_z = models.FloatField(default=0)
	saved_date_time = models.DateTimeField(default=timezone.now, null=True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Source(models.Model):
	source_doc = models.TextField(default='-')
	source_pointer = models.IntegerField(default=0)
	context = models.TextField(default='-')
	vector_distance_raw = models.FloatField(default=0)
	vector_score = models.FloatField(default=0)
	bm25_score_raw = models.FloatField(default=0)
	bm25_score = models.FloatField(default=0)
	rerank_score = models.FloatField(default=0)
	rank = models.IntegerField(default=0)
	secondary_rank = models.IntegerField(default=0)
	vector_distance_answer_raw = models.FloatField(default=0)
	vector_score_answer = models.FloatField(default=0)
	bm25_score_raw_answer = models.FloatField(default=0)
	bm25_score_answer = models.FloatField(default=0)
	rerank_entailment = models.TextField(default='-')
	chunk = models.ForeignKey(chunks, on_delete=models.CASCADE, null=True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.source_doc[:15] + ', p.' + str(self.source_pointer)

class Model(models.Model):
	model_name = models.CharField(max_length=200, default='-')
	model_size =  models.CharField(max_length=40, default='-')

	def __str__(self):
		return self.model_name
	
class EmbeddingModel(models.Model):
	model_name = models.CharField(max_length=200, default='-')
	model_size =  models.CharField(max_length=40, default='-')
	model_source = models.CharField(max_length=40, choices=embedding_model_source, default='ollama')
	best_distance_q = models.FloatField(default=0)
	worst_distance_q = models.FloatField(default=0)
	best_distance_ac = models.FloatField(default=0)
	worst_distance_ac = models.FloatField(default=0)
	best_distance_nac = models.FloatField(default=0)
	worst_distance_nac = models.FloatField(default=0)

	def __str__(self):
		return self.model_name
	
class RerankerModel(models.Model):
	model_name = models.CharField(max_length=200, default='-')
	cutoff_score = models.FloatField(default=0)

	def __str__(self):
		return self.model_name
	
class FrontEndSettings(models.Model):
	show_no_context_switch = models.BooleanField(default=False)
	azure_login = models.BooleanField(default=False)
	django_login = models.BooleanField(default=False)
	saved_date_time = models.DateTimeField(default=timezone.now, null=True)
	restriction_without_login = models.BooleanField(default=False)
	disable_chat_without_login = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = 'FrontEndSettings'
		verbose_name = 'FrontEndSettings'

class DisclaimerAgreement(models.Model):
	user = models.CharField(max_length=200, default='-')
	agreement_date_time = models.DateTimeField(default=timezone.now, null=True)