from django.conf.urls import url
from StoriesApp import views


urlpatterns = [
    url(r'^stories/$', views.AllStoriesView.as_view()),
    url(r'^stories/(?P<storie_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ConcreteStorieView.as_view()),
    url(r'^api/new_storie/$', views.new_storie, name='new_storie'),
	url(r'^$' , views.done, name = 'done'),
	url(r'^$' , views.nope, name = 'nope'),
]
