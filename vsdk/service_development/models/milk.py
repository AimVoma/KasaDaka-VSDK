from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from datetime import date, datetime

from .voicelabel import VoiceLabel, Language, VoiceFragment
from .vs_element import VoiceServiceElement



class Offer(models.Model):
	Message = models.FileField(upload_to=".")
	Date = models.DateTimeField(default=datetime.now, blank=True)
class Announcement(models.Model):
	Message = models.FileField(upload_to=".")
	Date = models.DateTimeField(default=datetime.now, blank=True)

class Record_offer(VoiceServiceElement):
	"""
	An element that presents a Voice Label to the user.
	"""
	_urls_name = 'service-development:record-offer'
	final_element = models.BooleanField('This element will terminate the call',default = False)
	_redirect = models.ForeignKey(
			VoiceServiceElement,
			on_delete = models.SET_NULL,
			null = True,
			blank = True,
			related_name='%(app_label)s_%(class)s_related',
			help_text = "The element to redirect to after the message has been played.")
	voice_label_confirm = models.ForeignKey(
			VoiceLabel,
			on_delete = models.SET_NULL,
			null = True,
			blank = True,
			)
	@property
	def redirect(self):
		"""
		Returns the actual subclassed object that is redirected to,
		instead of the VoiceServiceElement superclass object (which does
		not have specific fields and methods).
		"""
		if self._redirect :
			return VoiceServiceElement.objects.get_subclass(id = self._redirect.id)
		else: 
			return None

	def __str__(self):
		return "Record-offer: " + self.name

	def is_valid(self):
		return len(self.validator()) == 0
	is_valid.boolean = True

	def validator(self):
		errors = []
		errors.extend(super(Record_offer, self).validator())
		if not self.final_element and not self._redirect:
			errors.append('Message %s does not have a redirect element and is not a final element'%self.name)
		elif not self.final_element:
			if self._redirect.id == self.id:
				errors.append('!!!! There is a loop in %s'%str(self))
			else:
				errors.extend(self._redirect.validator())

		return errors
class Record_announcement(VoiceServiceElement):
	"""
	An element that presents a Voice Label to the user.
	"""
	_urls_name = 'service-development:record-announcement'
	final_element = models.BooleanField('This element will terminate the call',default = False)
	_redirect = models.ForeignKey(
			VoiceServiceElement,
			on_delete = models.SET_NULL,
			null = True,
			blank = True,
			related_name='%(app_label)s_%(class)s_related',
			help_text = "The element to redirect to after the message has been played.")
	voice_label_confirm = models.ForeignKey(
			VoiceLabel,
			on_delete = models.SET_NULL,
			null = True,
			blank = True,
			)
	@property
	def redirect(self):
		"""
		Returns the actual subclassed object that is redirected to,
		instead of the VoiceServiceElement superclass object (which does
		not have specific fields and methods).
		"""
		if self._redirect :
			return VoiceServiceElement.objects.get_subclass(id = self._redirect.id)
		else: 
			return None

	def __str__(self):
		return "Record-announcement: " + self.name

	def is_valid(self):
		return len(self.validator()) == 0
	is_valid.boolean = True

	def validator(self):
		errors = []
		errors.extend(super(Record_announcement, self).validator())
		if not self.final_element and not self._redirect:
			errors.append('Message %s does not have a redirect element and is not a final element'%self.name)
		elif not self.final_element:
			if self._redirect.id == self.id:
				errors.append('!!!! There is a loop in %s'%str(self))
			else:
				errors.extend(self._redirect.validator())

		return errors
