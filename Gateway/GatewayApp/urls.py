from django.conf.urls import url
from GatewayApp import views
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$' , views.main, name = 'main'),
    #url(r'^api/new_storie/$', views.new_storie, name='new_storie'),
    #url(r'^music/$' , views.music_list(), name = 'music_list'),
    url(r'^music/$' , views.MusicsView.as_view(), name = 'music_list'),
	#url(r'^$' , views.auth, name = 'auth'),
    url(r'^token-auth/$', views.AuthView.as_view()),
    url(r'^register/$', views.RegisterView.as_view()),
    url(r'^user_info/$', views.GetUserInfoView.as_view()),
    url(r'^users/$', views.UsersView.as_view()),
    url(r'^users/(?P<user_id>\d+)/$', views.ConcreteUserView.as_view()),

    url(r'^music/$', views.MusicsView.as_view()),
    url(r'^music/(?P<music_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ConcreteMusicView.as_view()),

    url(r'^stickers/$', views.StickersView.as_view()),
    url(r'^stickers/(?P<sticker_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ConcreteStickerView.as_view()),

    url(r'^stories/$', views.StoriesView.as_view()),
    url(r'^stories/(?P<storie_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ConcreteStorieView.as_view()),
]
