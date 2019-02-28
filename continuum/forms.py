from django import forms
from .models import Vote, Presupuesto, Project


class ProjectForm(forms.ModelForm):

	class Meta:
		model =Project
		fields = [ 'name', 'amount', 'active' ]

class VoteForm(forms.ModelForm):

	class Meta:
		model = Vote
		fields = [ 'project' ]