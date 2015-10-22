from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from . import views

urlpatterns = patterns('',
	url(r'^(?P<channel_slug>[a-z0-9-]+)/$', views.ChatRoomView, name='chatroom'),
	url(r'^(?P<channel_slug>[a-z0-9-]+)/feed/$', views.ChatRoomFeed, name='chatroom_feed'),
	url(r'^(?P<channel_slug>[a-z0-9-]+)/new/$', views.NewMessage, name='new_chatroom_message'),
)
