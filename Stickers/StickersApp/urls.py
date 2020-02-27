from django.conf.urls import url
from StickersApp import views


urlpatterns = [
    url(r'^stickers/$', views.StickersView.as_view()),
    url(r'^stickers/(?P<sticker_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ConcreteStickerView.as_view()),
]
