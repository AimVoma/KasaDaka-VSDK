from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.core.urlresolvers import reverse
from ..models import *

import time

def record_get_redirect_url(record_element,session):
    if not record_element.final_element:
        return record_element.redirect.get_absolute_url(session)
    else:
        return None



def record_generate_context(record_element, session, session_id, element_id, request):
    language = session.language
    premessage_voice_fragment_url = record_element.get_voice_fragment_url(language)
    postmessage_voice_fragment_url = record_element.get_voice_fragment_url(language)
    context = {'premessage_voice_fragment_url':premessage_voice_fragment_url,
               'postmessage_voice_fragment_url':postmessage_voice_fragment_url,
            'redirect_url':request.get_full_path()
               }
    return context


def record(request, element_id, session_id):
    record_element = get_object_or_404(Record_offer, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    context = record_generate_context(record_element, session, session_id, element_id, request)
    if request.method == 'GET':
        session.record_step(record_element)
        return render(request, 'recording_t.xml', context, content_type='text/xml')
    if request.method == 'POST':
        redirect_url = record_get_redirect_url(record_element,session)
        recording = request.FILES['recording']
        offer_obj = Offer(Message=recording)
        offer_obj.Message.name = 'recording_%s_%s_%s.wav' % (session_id, element_id,str(int(time.time())))
        offer_obj.save()
    return HttpResponseRedirect(redirect_url)


def get_voice_fragment_urlc(self, language):
    """
    Returns the url of the audio file of this element, in the given language.
    """
    return self.voice_label.get_voice_fragment_url(language)
