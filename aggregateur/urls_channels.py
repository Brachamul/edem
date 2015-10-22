from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
	url(r'^$', views.channel_list, name='public_channels'),
	url(r'^mes-chaines$', views.channel_list, {'channels': 'my-channels'}, name='my_channels'),
	url(r'^creer$', views.nouvelle_chaine, name='nouvelle_chaine'),
	url(r'^(?P<channel_slug>[a-z0-9-]+)/rejoindre$', views.join_channel, name='join_channel'),
	url(r'^(?P<channel_slug>[a-z0-9-]+)/quitter$', views.leave_channel, name='leave_channel'),
	url(r'^(?P<channel_slug>[a-z0-9-]+)/candidats$', views.wanttojoin_channel, name='wanttojoin_channel'),
	url(r'^(?P<channel_slug>[a-z0-9-]+)/autoriser/(?P<user_pk>\d+)$', views.allow_user_to_join_channel, name='allow_user_to_join_channel'),
	url(r'^(?P<channel_slug>[a-z0-9-]+)/refuser/(?P<user_pk>\d+)$', views.deny_user_from_channel, name='deny_user_from_channel'),
	url(r'^(?P<channel_slug>[a-z0-9-]+)$', views.aggregateur, name='chaine'),
	url(r'^(?P<channel_slug>[a-z0-9-]+)/(?P<page>[0-9]+)/$', views.aggregateur, name='channel_page'),

)