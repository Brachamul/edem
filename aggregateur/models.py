from math import sqrt

from django.conf import settings
from django.db import models
from django.utils import timezone

from autoslug.fields import AutoSlugField

from django.contrib.auth.models import User

class Settings(models.Model):
	''' We'll use this to manage settings from inside the app
		Only the first instance of this model will be used '''
	main_settings = models.BooleanField(unique=True, default=True)
	welcome_text = models.TextField(max_length=1024, default="Bienvenue sur Élan Démocrate.")


class Channel(models.Model):
	name = models.CharField(max_length=32, verbose_name="nom", unique=True)
	slug = AutoSlugField(populate_from=('name'), unique=True, editable=True, max_length=64)
	date = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=255)
	is_official = models.BooleanField(default=False, verbose_name='Officielle')
	is_default = models.BooleanField(default=False, verbose_name='Par défaut') # If a channel is default, it will be seen by users without needing subscription
	is_private = models.BooleanField(default=False, verbose_name='Privée') # If a channel is private, only moderators and subscribers will see it
	only_mods_can_post = models.BooleanField(default=False, verbose_name='Seuls les modérateurs peuvent poster') # For channels that are for downwards communications
	moderators = models.ManyToManyField(User, related_name='moderated_channels', blank=True)
	subscribers = models.ManyToManyField(User, related_name='subscribed_channels', blank=True)
	ignorers = models.ManyToManyField(User, related_name='ignored_channels', blank=True) # users can still choose not to view the channel if they wish
	want_to_join = models.ManyToManyField(User, related_name='applied_to_channels', blank=True, through='WantToJoinChannel')
	illustration = models.URLField(default=settings.SITE_URL+"/static/images/default_channel_illustration.png")
	def __str__(self): return self.name
	class Meta:
		 ordering = ['-is_default']

class WantToJoinChannel(models.Model):
	''' We have a specific M2M model so that we can easily send
		a notification signal when this is changed '''
	user = models.ForeignKey(User)
	channel = models.ForeignKey(Channel)


class Post(models.Model):
	date = models.DateTimeField(default=timezone.now)
	format = models.CharField(max_length=255, choices=(("LINK", "link"), ("TEXT", "text")))
	title = models.CharField(max_length=144)
	slug = AutoSlugField(populate_from=('title'), unique_with='date__year', max_length=255)
	content = models.TextField(max_length=10000, null=True, blank=True)
	author = models.ForeignKey(User)
	channel = models.ForeignKey(Channel, null=True, blank=True)
	is_pinned = models.BooleanField(default=False, verbose_name='Maintenir en haut')
	last_edit = models.DateTimeField(null=True, blank=True)
	deleted = models.BooleanField(default=False)
	health = models.IntegerField(default=0) # votes positifs - votes négatifs
	rank = models.IntegerField(default=0) # rang selon l'algorithme, prenant en compte le temps passé
	illustration = models.URLField(max_length=2000, null=True, blank=True)
	shareable = models.BooleanField(default=True)
	def __str__(self): return self.title
	class Meta:
		 ordering = ['-is_pinned', '-rank', '-date']

class Vote(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	color = models.CharField(max_length=24, choices=(("POS", "positif"), ("NEG", "négatif"), ("NEU", "neutre")))
	def __str__(self): return self.color

class LastRanking(models.Model):
	date = models.DateTimeField()



class Comment(models.Model):

	content = models.TextField(max_length=10000)
	author = models.ForeignKey(User)
	date = models.DateTimeField(default=timezone.now)
	last_edit = models.DateTimeField(null=True, blank=True)
	parent_post = models.ForeignKey(Post, null=True, blank=True)
	parent_comment = models.ForeignKey('self', null=True, blank=True)
	deleted = models.BooleanField(default=False)
	health = models.IntegerField(default=0) # votes positifs - votes négatifs
	rank = models.IntegerField(default=0) # rang selon l'algorithme, prenant en compte le temps passé

	def __str__(self): return self.content

	def post_racine(self):
		'''récupère le post auquel ce commentaire est rattaché'''
		parent_post = None
		comment = self
		while parent_post == None :
			parent_post = comment.parent_post
			if not parent_post : comment = comment.parent_comment
		return parent_post

	def profondeur(self):
		'''renvoie le niveau de profondeur de se post par rapport à sa racine'''
		profondeur = 0
		parent_post = None
		comment = self
		while parent_post == None :
			profondeur += 1
			parent_post = comment.parent_post
			if not parent_post : comment = comment.parent_comment
		return profondeur

	def evaluer_le_score(self):
		POS = CommentVote.objects.filter(comment=self, color="POS").count()
		NEG = CommentVote.objects.filter(comment=self, color="NEG").count()
		n = POS + NEG # >>> Nombre de votes
		if n == 0 :
			score = 0
		else :
			z = 1.0  #1.0 = 85%, 1.6 = 95% >>> Niveau de confiance requis
			phat = float(POS) / n 
			score = sqrt(phat+z*z/(2*n)-z*((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n) # Dafuq
		self.rank = score
		return score



class CommentVote(models.Model):
	user = models.ForeignKey(User)
	comment = models.ForeignKey(Comment)
	color = models.CharField(max_length=24, choices=(("POS", "positif"), ("NEG", "négatif"), ("NEU", "neutre")))
	def __str__(self): return self.color