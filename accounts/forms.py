from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib import auth

from models import OneShotGoal, OneShotJournal, OneShotNote


class OneShotGoalForm(forms.ModelForm):
	"""
	Form for creating one shot goals
	"""
	
	title = forms.RegexField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Title*'}), max_length=75, regex=r'[^\@\.\/+)(*&^%$#!\[\]:{}\'";,<>?|]+$', error_messages={'invalid': "Invalid Title."})
	description = forms.CharField(max_length=300, required = False, label='', widget=forms.Textarea(attrs={'placeholder': 'Goal Description'}))
	private = forms.BooleanField(required=False, label='Private')
	completed = forms.BooleanField(required=False, label='Completed')
	date_completed = forms.DateField(required=False, label='MM/DD/YYYY')

	class Meta:
		model = OneShotGoal
		fields = ('title', 'description', 'private', 'completed', 'date_completed',)
	
	def clean_title(self):
		"""
		Validate title and see if it's in use.
		"""
		title = self.cleaned_data['title']
		
		if title[0] == ' ':
			raise forms.ValidationError('Cannot lead with a space.')
		elif '%20' in title:
			raise forms.ValidationError('Invalid title.')
		elif OneShotGoal.objects.exclude(pk=self.instance.pk).filter(title=title).exists():
			raise forms.ValidationError('You already have a goal by this title.')
		else:
			return title
	
	def clean_completed(self):
		"""
		Raise Error if date_completed has something when the goal is not yet completed and vice versa
		"""
		
		date_completed = self.cleaned_data.get('date_completed')
		completed = self.cleaned_data.get('completed')
		if completed and (date_completed is None):
			raise forms.ValidationError('Please enter a date of completion')
		else:
			if completed and (not (date_completed is None)):
				return completed
			else:
				if (not completed) and (date_completed is None):
					return completed
				else:
					raise forms.ValidationError('If goal is completed, please check it off')
				
	def clean_date_completed(self):
		"""
		Raise Error if date_completed is greater than the current date.
		"""
		date_completed = self.cleaned_data.get('date_completed')
		if (date_completed is None):
			return date_completed
		else:
			if (datetime.now().date() < date_completed):
				raise forms.ValidationError('Time travel is not allowed.')
			else:
				return date_completed

class OneShotJournalForm(forms.ModelForm):
	"""
	Form for creating journal entries for one shot goals
	"""
	
	entry = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Journal Entry'}))

	class Meta:
		model = OneShotJournal
		fields = ('entry',)
		
class OneShotNoteForm(forms.ModelForm):
	"""
	Form for creating notes for one shot goals
	"""
	
	note = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Note'}))
	
	class Meta:
		model = OneShotNote
		fields = ('note',)