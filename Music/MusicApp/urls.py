from django.conf.urls import url
from MusicApp import views


urlpatterns = [
    url(r'^music/$', views.MusicsView.as_view()),
    url(r'^music/(?P<music_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ConcreteMusicView.as_view()),
]
