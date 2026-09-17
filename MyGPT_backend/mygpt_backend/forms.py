from django.forms import ModelForm
from .models import Papers

class PapersForm(ModelForm):
	class Meta:
		model = Papers
		fields = ['paper_title', 'paper_attachment']
