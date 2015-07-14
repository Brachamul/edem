from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from fichiers_adherents.models import Adhérent

import string, random
def randomly_generated_code(i): return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(i))
	# http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python

from datetime import datetime, timedelta
class Credentials(models.Model):
	user = models.OneToOneField(User) # credentials are linked to one specific user
	code = models.CharField(max_length=settings.AUTH_CODE_LENGTH, default=randomly_generated_code(settings.AUTH_CODE_LENGTH))
	date = models.DateTimeField(auto_now=True)
	attempts = models.PositiveSmallIntegerField(default=0) # increments each time a user attempts to log in with a code
	def is_expired(self): return not (self.date > (datetime.now() - timedelta(hours=settings.AUTH_CODE_LIFESPAN))) # Code is active for 4 hours
	def too_many_attempts(self): return (self.attempts >= settings.AUTH_CODE_MAXIMUM_ATTEMPS)
	def regenerate(self):
		self.code = self.code.default
		self.date = datetime.now()
		self.attempts = self.code.default
		self.save()
	class Meta :
		verbose_name_plural = "Credentials"

class EmailConfirmationInstance(models.Model):
	adherent = models.ForeignKey(Adhérent) # credentials are linked to one specific user
	email = models.EmailField() # we'll send them an email !
	code = models.CharField(max_length=32, default=randomly_generated_code(32))
	date = models.DateTimeField(auto_now=True)


### maybe enable phone numbers at some point ?
#   phone_regex = RegexValidator(
#	   regex=r'^\+?1?\d{9,15}$', 
#	   message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
#	   )
#   phone_number = models.CharField(validators=[phone_regex], blank=True)