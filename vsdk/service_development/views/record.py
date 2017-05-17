from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *


def record_options_resolve_redirect_urls(record_options, session):
    record_options_redirection_urls = []
    for record_option in record_options:
        redirect_url = record_option.redirect.get_absolute_url(session)
        record_options_redirection_urls.append(redirect_url)
    return record_options_redirection_urls

def record_options_resolve_voice_labels(record_options, language):
    """
    Returns a list of voice labels belonging to the provided list of record_options.
    """
    record_options_voice_labels = []
    for record_option in record_options:
        record_options_voice_labels.append(record_option.get_voice_fragment_url(language))
    return record_options_voice_labels

def record_generate_context(record_element, session):
    """
    Returns a dict that can be used to generate the record VXML template
    record = this record element object
    record_voice_label = the resolved Voice Label URL for this record element
    record_options = iterable of recordOption object belonging to this record element
    record_options_voice_labels = list of resolved Voice Label URL's referencing to the record_options in the same position
    record_options_redirect_urls = list of resolved redirection URL's referencing to the record_options in the same position
        """
    record_options =  record_element.record_options.all()
    language = session.language
    context = {'record':record_element,
                'record_voice_label':record_element.get_voice_fragment_url(language),
                'record_options': record_options,
                'record_options_voice_labels':record_options_resolve_voice_labels(record_options, language),
                    'record_options_redirect_urls': record_options_resolve_redirect_urls(record_options,session),
                    'language': language,
                    }
    return context

def record(request, element_id, session_id):
    if request.method == 'GET':
        record_element = get_object_or_404(Record, pk=element_id)
        session = get_object_or_404(CallSession, pk=session_id)
        session.record_step(record_element)
        context = record_generate_context(record_element, session)
    
        return render(request, 'record.xml', context, content_type='text/xml')
    if request.method == 'POST':
        pass


