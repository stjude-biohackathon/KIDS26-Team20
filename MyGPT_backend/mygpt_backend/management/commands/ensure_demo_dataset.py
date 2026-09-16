from django.core.management.base import BaseCommand

from mygpt_backend.models import Dataset
from mygpt_backend.views.dataset_management import add_demo_dataset


class Command(BaseCommand):
    help = 'Add the Turing Way demo dataset when it does not exist'

    def handle(self, *args, **options):
        if Dataset.objects.filter(dataset_name='Turing_Way').exists():
            self.stdout.write('Turing_Way demo dataset already exists')
            return

        add_demo_dataset()
        self.stdout.write(self.style.SUCCESS('Added Turing_Way demo dataset'))