from django.conf.urls import url

from . import views

urlpatterns=[

	url(r'^create/', views.create,name='create'),
	url(r'^$', views.home,name='home'),
	url(r'^(?P<pk>[0-9]+)/upvote', views.upvote,name='upvote'),
	url(r'^(?P<pk>[0-9]+)/downvote', views.downvote,name='downvote'),
	url(r'^user/(?P<pk>[0-9]+)/', views.userposts,name='userposts'),
]