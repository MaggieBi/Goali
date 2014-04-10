from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib import auth

class RegisterForm(forms.ModelForm):
	"""
	Form for registering new user account
	"""
	username = forms.RegexField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}), max_length=30, regex=r'[^\@\.\/+)(*&^%$#!\[\]:{}\'";,<>?|]+$', error_messages={'invalid': "Usernames may contain only letters and numbers."})
	email = forms.EmailField(max_length=75, required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	password1 = forms.CharField(max_length=70, required = True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(max_length=70, required = True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))

	class Meta:
		model = User
		fields = ('username', 'email',)
	
	def clean_username(self):
		"""
		Validate the username to be alphanumeric and see if it's in use.
		"""
		username = self.cleaned_data['username']
		if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
			raise forms.ValidationError('This username is already taken.')
		else:
			return username
	
	def clean_email(self):
		"""
		Validates that the email isn't in use
		"""
		email = self.cleaned_data['email']
		if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
			raise forms.ValidationError('This email is already registered.')
		else:
			return email
			
	def clean_password2(self):
		"""
		Validate that the two passwords match
		"""
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Your passwords don't match.")
		return password2
	
	def save(self, commit = True):
		"""
		Save values and return object for storing
		"""
		user = super(RegisterForm, self).save(commit = False)
		user.username = self.cleaned_data['username']
		user.email = self.cleaned_data['email']
		user.set_password(self.cleaned_data['password1'])
		
		if commit:
			user.save()
		return user

class LoginForm(forms.Form):
	"""
	Form for logging in user account
	"""
	username = forms.CharField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Username or Email'}), max_length=75)
	password = forms.CharField(max_length=70, required = True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
		
	class Meta:
		model = User
		fields = ('username',)

	def clean_password(self):
		"""
		Validate the user password combination.
		"""
		username = self.cleaned_data['username']
		password = self.cleaned_data.get("password")
		if not "@" in username:
			if User.objects.filter(username=username).exists():
				try:
					user = User.objects.get(username=username)
					if user.check_password(password):
						return password
					else:
						raise forms.ValidationError('Incorrect password.')
				except User.DoesNotExist:
					raise forms.ValidationError('User does not exist.')
			else:
				raise forms.ValidationError('Username does not exist.')
		else:
			if User.objects.filter(email=username).exists():
				try:
					user = User.objects.get(email=username)
					if user.check_password(password):
						return password
					else:
						raise forms.ValidationError('Incorrect password.')
				except User.DoesNotExist:
					raise forms.ValidationError('Email is not registered.')
			else:
				raise forms.ValidationError('Email is not registered.')
	
	
	def get_user(self, username):
		"""
		Returns the user based on email.
		"""
		try:
			return User.objects.filter(email=username).get()
		except User.DoesNotExist:
			return None
	
class ContactForm(forms.Form):
	subject = forms.CharField(max_length=100, label='Subject')
	email = forms.EmailField(required=False, label='E-Mail Address (optional)')
	message = forms.CharField(widget=forms.Textarea, label='Subject')
	
