from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.test import Client
from django.urls import reverse
from rest_framework.test import APIClient

from mygpt_backend.models import Dataset, Papers


@pytest.mark.django_db
class TestModels:
	# test models
	def test_dataset(self):
		# check dataset model
		dataset = Dataset.objects.all()
		assert len(dataset) == 0

	def test_papers(self):
		# check papers model
		papers = Papers.objects.all()
		assert len(papers) == 0


@pytest.mark.django_db
class TestEnsureDemoDatasetCommand:
	@patch('mygpt_backend.management.commands.ensure_demo_dataset.add_demo_dataset')
	def test_adds_demo_dataset_when_missing(self, add_demo_dataset_mock):
		call_command('ensure_demo_dataset')

		add_demo_dataset_mock.assert_called_once_with()

	@patch('mygpt_backend.management.commands.ensure_demo_dataset.add_demo_dataset')
	def test_skips_existing_demo_dataset(self, add_demo_dataset_mock):
		Dataset.objects.create(dataset_name='Turing_Way')

		call_command('ensure_demo_dataset')

		add_demo_dataset_mock.assert_not_called()

@pytest.mark.django_db
class TestAPI:
	def test_dataset(self):
		# check dataset api
		client = APIClient()
		response = client.get('/api/')
		assert response.status_code == 200

	def test_papers(self):
		# check papers api
		client = APIClient()
		response = client.get('/api/papers/')
		assert response.status_code == 200

	def test_datasets(self):
		# check datasets api
		client = APIClient()
		response = client.get('/api/datasets/')
		assert response.status_code == 200

	def test_questions(self):
		# check questions api
		client = APIClient()
		response = client.get('/api/questions/')
		assert response.status_code == 200

	def test_answers(self):
		# check answers api
		client = APIClient()
		response = client.get('/api/answers/')
		assert response.status_code == 200

@pytest.mark.django_db
class TestViews:
	def test_admin(self):
		# check admin view
		client = Client()
		response = client.get('/admin/')
		assert response.status_code == 302

	def test_get_papers(self):
		# check get_papers view
		client = Client()
		url = reverse('get_paper')
		response = client.get(url)
		print(response)
		assert response.status_code == 200

	def test_papers_with_dataset(self):
		# check papers with dataset view
		client = Client()
		Dataset.objects.create(dataset_name='GPCR', zotero_id='1234', dataset_size=10)
		Papers.objects.create(paper_title='test', paper_dataset=Dataset.objects.get(dataset_name='GPCR'))
		url = reverse('get_paper')
		response = client.get(url, {'dataset': 'GPCR'})
		papaers = response.json()
		assert response.status_code == 200
		assert len(papaers) == 1

	@patch('mygpt_backend.views.apis.add_demo_dataset')
	def test_add_demo_dataset_preserves_existing_dataset(
		self, add_demo_dataset_mock
	):
		Dataset.objects.create(dataset_name='Turing_Way')

		response = Client().get(reverse('add_demo_dataset'))

		assert response.status_code == 200
		assert Dataset.objects.filter(dataset_name='Turing_Way').exists()
		add_demo_dataset_mock.assert_called_once_with('multi-qa-MiniLM-L6-cos-v1')
		
