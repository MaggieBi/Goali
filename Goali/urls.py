from django.conf.urls import patterns, include, url
from Goali.views import homepage, login_new, logout
from accounts.views import myprofile
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	#homepage
	url(r'^$', homepage, name='homepage'),
	
	
	#admin-site
	url(r'^admin/', include(admin.site.urls)),
	
	#login / logout
	url(r'^login_new/', login_new, name='login_new'),
	url(r'^logout/', logout, name='logout'),	
	
	#Personal account login
	url(r'^(?P<username>.+?)/$', myprofile, name='myprofile'),
	
)
