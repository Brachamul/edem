from django.contrib.auth.models import User
from aggregateur.models import Channel
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Message(models.Model):
	channel = models.ForeignKey(Channel)
	author = models.ForeignKey(User)
	content = models.CharField(max_length=1024)
	date = models.DateTimeField(auto_now_add=True)
	def __str__(self) : return self.author.profil.nom_courant + ' on ' + self.channel.name + ' : ' + self.content
	class Meta:
		ordering = ['-date',]