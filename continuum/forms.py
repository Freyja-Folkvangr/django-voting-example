from django import forms
from .models import Presupuesto, Project, Votes



class ProjectForm(forms.ModelForm):

	class Meta:
		model =Project
		fields = [ 'name', 'amount', 'active' ]

class VoteForm(forms.ModelForm):

	class Meta:
		model = Votes
		fields = [ 'name', 'votes' ]