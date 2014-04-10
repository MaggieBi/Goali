from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def myprofile(request, username):
	username=request.user.username
	try:
		user = User.objects.filter(username=username).get()
	except User.DoesNotExist:
		user = None
	return render(request, 'profile.html', {'user' : user})