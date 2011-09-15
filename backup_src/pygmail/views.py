from django.template import Context, loader, RequestContext
from polls.models import Choice, Poll
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

def contact_us(request):
    user_profile = request.user.get_profile()
    url = user_profile.url
