from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from aggregateur.views import aggregateur

admin.site.site_header = 'Élan Démocrate - Administration'

urlpatterns = patterns('',
	url(r'^$', aggregateur, name='accueil'),
	url(r'^auth/', include('auth_with_one_time_code.urls')),
	url(r'^m/', include('membres.urls')),
	url(r'^p/', include('aggregateur.urls')),
	url(r'^c/', include('aggregateur.urls_channels')),
	url(r'^tout/', aggregateur, {'special': "all_channels"}, name='all_channels'),
	url(r'^defaut/', aggregateur, {'special': "default_channels"}, name='default_channels'),
	url(r'^n/', include('notifications.urls')),
	url(r'^d/', include('datascope.urls')),
	url(r'^beta/', include('beta.urls')),
	url(r'^tableau-de-bord/', include('tableau_de_bord.urls')),
	url(r'^fichiers-adherents/', include('fichiers_adherents.urls')),
	url(r'^mandats/', include('mandats.urls')),
	url(r'^chat/', include('chatrooms.urls')),
	url(r'^admin/', include(admin.site.urls), name='admin'),
)

from django.conf import settings
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': settings.MEDIA_ROOT}))

urlpatterns += patterns('',
	#
	)