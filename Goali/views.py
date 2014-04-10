import datetime, random, hashlib
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import Template, Context
from django.template.loader import get_template
from django.contrib.sessions.models import Session
from django.contrib.auth import login, logout

from forms import RegisterForm, LoginForm, ContactForm
from accounts.models import User

def homepage(request):
	"""
	Register a new user. Salt hash (use sha) and email them an activation key
	"""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/%s/'%request.user.username)
	else:
		if request.method == 'POST':
			if 'registerSub' in request.POST:
				registerform = RegisterForm(request.POST)
				loginform = LoginForm()
				if registerform.is_valid():
					#Make activation key, STILL NEED TO WRITE VIEW FOR CONFIRMATION
					#salt = sha.new(str(random.random())).hexdigest()[:5]
					#activation_key = sha.new(salt+new_user.username).hexdigest()
					#key_expires = datetime.datetime.today() + datetime.timedelta(92)
					
					#save new user
					new_user = registerform.save()

					#send email
					#email_subject = 'Your Goali Account Confirmation'
					#email_body = "Hello, %s! Thank you for signing up for a Goali account!\nTo activate your account, click this link within 48 \hours:\n\nhttp://example.com/accounts/confirm/%s" % (new_user.username,new_profile.activation_key)
					#send_mail(email_subject,email_body,'admin@goali.net',[new_user.email])
					
					return HttpResponseRedirect('/%s/'%request.user.username)
			elif 'loginSub' in request.POST:
				try:
					loginform = LoginForm(request.POST)
					registerform = RegisterForm()
					if loginform.is_valid():
						username = request.POST.get('username', '')
						password = request.POST.get('password', '')
						if not "@" in username:
							user = auth.authenticate(username=username, password=password)
							#if user is not None and user.is_active:
							if user is not None:
								if user.is_active:
									auth.login(request, user)
	#								request.sessions['member_id'] = m.id
									return HttpResponseRedirect('/%s/'%request.user.username)
								else:
									return HttpResponseRedirect('your account is not active, please contact the site administrator')
							else:
								HttpResponse("your username and password are incorrect")
						else:
							acct = loginform.get_user(username)
							user = auth.authenticate(username=acct, password=password)
							if user is not None:
								if user.is_active:
									auth.login(request, user)
	#								request.sessions['member_id'] = m.id
									return HttpResponseRedirect('/%s/'%request.user.username)
								else:
									return HttpResponseRedirect('your account is not active, please contact the site administrator')
							else:
								HttpResponse("your username and password are incorrect")	
				except User.DoesNotExist:
					return HttpResponse("Your username and password didn't match.")
		else:
			registerform = RegisterForm()
			loginform = LoginForm()
		return render(request, "homepage.html", { 'registerform': registerform, 'loginform': loginform } )

def login_new(request):
	"""
	Login as a new user. Still needs to be finished.
	"""
	return HttpResponseRedirect("/")

def logout(request):
	"""
	Logout
	"""
	auth.logout(request)
	return HttpResponseRedirect("/")
	
#contact web owner
def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			send_mail(
				cd['subject'],
				cd['message'],
				cd.get('email', 'noreply@example.com'),
				['siteowner@example.com'],
			)
		return HttpResponseRedirect('/contact/thanks/')
	else:
		form = ContactForm()
	return render(request, 'contact_form.html', {'form': form})

