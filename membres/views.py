from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.views import generic
from django.views.generic import TemplateView, DetailView

from .models import *
from django.contrib.auth.models import User
from fichiers_adherents.models import Adherent
from mandats.models import Detenteur
from mandats.views import pecho_les_mandats
#from mandats.forms import NouveauMandatForm
from auth_with_one_time_code import backend

### Profile

@login_required
def profil(request, pk):
	try : user = User.objects.get(pk=pk)
	except User.DoesNotExist : raise Http404("Cet utilisateur n'existe pas.")
	else :
		try : profil = Profil.objects.get(user=user)
		except Profil.DoesNotExist : raise Http404("Ce profil n'existe pas.")
		else :
			if request.method == "POST" :
				if user == request.user or request.user.is_staff : process_profil_changes(request, user, profil)
			profil.mandats = pecho_les_mandats(profil)
			return render(request, 'membres/profil.html', {'membre': user, 'profil': profil, 'page_title': profil.nom_courant})

def process_profil_changes(request, user, profil) :

	changes = False # Il n'y a pas eu de changement, par défaut

	if request.POST.get('bio') :
		profil.bio = request.POST.get('bio')
		profil.save()
		changes = True

	if request.POST.get('nom_courant') :
		profil.nom_courant = request.POST.get('nom_courant')
		profil.save()
		changes = True

	if request.POST.get('twitter') :
		profil.twitter = request.POST.get('twitter').strip('@').strip(' ')
		profil.save()
		changes = True

	messages.success(request, "Vos modifications ont bien été prises en compte.")

def actorCard(request, pk): return render(request, 'actor.html', { 'actor': get_object_or_404(User, pk=pk), } )