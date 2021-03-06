from django import forms
from .models import Choice, Votes, Question



class create_choice_form(forms.ModelForm):

	class Meta:
		model = Choice
		fields = [ 'question', 'choice_text', 'description', 'cost']

class vote_form(forms.ModelForm):

	class Meta:
		model = Votes
		fields = [ 'name', 'process', 'votes' ]

class create_question_form(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['question_text', 'budget']