from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


from .voicelabel import VoiceLabel, Language, VoiceFragment
from .vs_element import VoiceServiceElement



class Consumers(models.Model):
	Credentials = models.FileField(help_text = "Ensure your file is in the correct format! Wave: Sample rate 8KHz, 16 bit, mono, Codec: PCM 16 LE (s16l)")
	Date = models.CharField(max_length=100)
	product = models.FileField(help_text = "Ensure your file is in the correct format! Wave: Sample rate 8KHz, 16 bit, mono, Codec: PCM 16 LE (s16l)")

class Producers(models.Model):
	Credentials = models.FileField(help_text = "Ensure your file is in the correct format! Wave: Sample rate 8KHz, 16 bit, mono, Codec: PCM 16 LE (s16l)")
	Date = models.CharField(max_length=100)
	product = models.FileField(help_text = "Ensure your file is in the correct format! Wave: Sample rate 8KHz, 16 bit, mono, Codec: PCM 16 LE (s16l)")