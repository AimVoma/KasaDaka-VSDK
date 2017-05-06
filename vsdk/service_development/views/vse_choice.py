from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.core.urlresolvers import reverse
from ..models import *
from . import *
def record_get_redirect_url(record_element,session):
	if not record_element.final_element:
		return record_element.redirect.get_absolute_url(session)
	else:
		return None
	
def record_generate_context(record_element, session, session_id, element_id, request):

	language = session.language
	premessage_voice_fragment_url = record_element.get_voice_fragment_url(language)
	postmessage_voice_fragment_url = record_element.voice_label_confirm.get_voice_fragment_url(language)
	context = {'premessage_voice_fragment_url':premessage_voice_fragment_url,
		'postmessage_voice_fragment_url':postmessage_voice_fragment_url,
			'redirect_url':request.get_full_path()}
	return context


def record_announcement(request, element_id, session_id):

	record_element = get_object_or_404(Record_announcement, pk=element_id)
	session = get_object_or_404(CallSession, pk=session_id)
	context = record_generate_context(record_element, session, session_id, element_id, request) 
	if request.method == 'GET':
		session.record_step(record_element)   
		return render(request, 'recording_t.xml', context, content_type='text/xml')
	if request.method == 'POST':
		redirect_url = record_get_redirect_url(record_element,session)
		#for now the upload recording functionalities is not active
		#print(request.FILES)
		#recording = request.FILES['recording']
		#recording.name='announcement_%s_%s.wav' % (session_id, session.caller_id)
		#t=type(recording)
		#print(recording)
		#announcement = Announcement(Message=recording)
		#announcement.save()
		return HttpResponseRedirect(redirect_url)

def record_offer(request, element_id, session_id):

	record_element = get_object_or_404(Record_offer, pk=element_id)
	session = get_object_or_404(CallSession, pk=session_id)
	context = record_generate_context(record_element, session, session_id, element_id, request) 
	if request.method == 'GET':
		session.record_step(record_element)   
		return render(request, 'recording_t.xml', context, content_type='text/xml')
	if request.method == 'POST':
		redirect_url = record_get_redirect_url(record_element,session)
		#for now the upload recording functionalities is not active
		#print(request.FILES)
		#recording = request.FILES['recording']
		#recording.name='offer_%s_%s.wav' % (session_id, session.caller_id)
		#t=type(recording)
		#print(recording)
		#offer = Offer(Message=recording)
		#offer.save()
		return HttpResponseRedirect(redirect_url)

def choice_options_resolve_redirect_urls(choice_options, session):
	choice_options_redirection_urls = []
	for choice_option in choice_options:
		redirect_url = choice_option.redirect.get_absolute_url(session)
		choice_options_redirection_urls.append(redirect_url)
	return choice_options_redirection_urls

def choice_options_resolve_voice_labels(choice_options, language):
	"""
	Returns a list of voice labels belonging to the provided list of choice_options.
	"""
	choice_options_voice_labels = []
	for choice_option in choice_options:
		choice_options_voice_labels.append(choice_option.get_voice_fragment_url(language))
	return choice_options_voice_labels

def choice_generate_context(choice_element, session):
	"""
	Returns a dict that can be used to generate the choice VXML template
	choice = this Choice element object
	choice_voice_label = the resolved Voice Label URL for this Choice element
	choice_options = iterable of ChoiceOption object belonging to this Choice element
	choice_options_voice_labels = list of resolved Voice Label URL's referencing to the choice_options in the same position
	choice_options_redirect_urls = list of resolved redirection URL's referencing to the choice_options in the same position
		"""
	choice_options =  choice_element.choice_options.all()
	language = session.language
	context = {'choice':choice_element,
				'choice_voice_label':choice_element.get_voice_fragment_url(language),
				'choice_options': choice_options,
				'choice_options_voice_labels':choice_options_resolve_voice_labels(choice_options, language),
				'choice_options_redirect_urls': choice_options_resolve_redirect_urls(choice_options,session),
				'voice_label_no_input': choice_element.voice_label_no_input.get_voice_fragment_url(language),
				'language': language,
					}
	return context

def choice(request, element_id, session_id):
	choice_element = get_object_or_404(Choice, pk=element_id)
	session = get_object_or_404(CallSession, pk=session_id)
	session.record_step(choice_element)
	context = choice_generate_context(choice_element, session)
	
	return render(request, 'choice.xml', context, content_type='text/xml')

