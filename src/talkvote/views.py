import json
from datetime import datetime, timedelta, date
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.template import loader, RequestContext
from django.utils import simplejson
from django.contrib.auth import authenticate, login
from django.db.models.query import QuerySet
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers

from confreg.views import payment_required
from confreg.models import ConfRegModel
from talkvote.models import VoteRecord
from talksub.models import TalkSubmission,UserTalkProfile,TalkSchedule

from talksub.models import TalkSubmission
from settings import MEDIA_URL

VOTE_DIRECTIONS = (('up', 1), ('down', -1), ('no_repeat',0))


@login_required
@payment_required
def confirm(request, object_id):
        p = get_object_or_404(Talks, pk=object_id)
        return render_to_response('talkvote/confirm.html', {'talk':p})

@login_required
@payment_required
def one_vote(request):
        return render_to_response('talkvote/one_vote.html')

def invited_speaker_talks(request):
	inv_speakers = UserTalkProfile.objects.filter(invited_speaker=True).values('author')
	talks = TalkSubmission.objects.filter(author__in = inv_speakers)
	names = ConfRegModel.objects.filter(user__in = inv_speakers)
	for talk in talks:
		talk.full_name = names.filter(user = talk.author).values('full_name')[0]['full_name']
        return render_to_response('talkvote/generic_talk_list.html',
            {'talks':talks,
             'desc_title':'Scheduled Talks Entered So Far (more soon)',
             'paginate_by':1000,
             'allow_empty':True,
             'MEDIA_URL':MEDIA_URL},
             context_instance=RequestContext(request))

def proposed_to_be_voted_talks(request):
	registrants = UserTalkProfile.objects.filter(invited_speaker=False).values('author')
	talks = TalkSubmission.objects.filter(author__in = registrants)
	names = ConfRegModel.objects.filter(user__in = registrants)
	for talk in talks:
		talk.full_name = names.filter(user = talk.author).values('full_name')[0]['full_name']
        return render_to_response('talkvote/generic_talk_list.html',
            {'talks':talks,
             'desc_title':'Talks Proposed for Vote',
             'paginate_by':1000,
             'allow_empty':True,
             'MEDIA_URL':MEDIA_URL},
             context_instance=RequestContext(request))

def full_schedule(request):
	names = ConfRegModel.objects.all()
	schedule = TalkSchedule.objects.order_by('talk_day_time')
	for_json = []
	day_1 = []
	day_2 = []
	for s in schedule:
		s.end_time = s.talk_day_time + timedelta(minutes=s.duration_minutes)
		s.talk.full_name = names.filter(user = s.talk.author).values('full_name')[0]['full_name']
		day_1.append(s) if s.talk_day_time.date().day == 16 else day_2.append(s)
		for_json.append({
		    'full_name':s.talk.full_name,
		    'talktype':s.talk.talktype,
		    'title':s.talk.title,
		    'levels': [str(x) for x in s.talk.levels.all()],
		    'outline':s.talk.outline,
		    'desc':s.talk.desc,
		    'talk_day_time':str(s.talk_day_time),
		    'duration_minutes':s.duration_minutes,
		    'talk_end_time':str(s.end_time),
		    'room_number':s.room,
		    'key':"%s_%s" % (s.id,s.talk.id)
			})

	if request.accepted_types[0] == 'application/json':
		return HttpResponse(json.dumps(for_json), mimetype="application/json")

        return render_to_response('talkvote/full_schedule.html',
            {'day_1':day_1,
             'day_2':day_2, 
             'desc_title':'Full Schedule',
             'paginate_by':1000,
             'allow_empty':True,
             'MEDIA_URL':MEDIA_URL},
             context_instance=RequestContext(request))

@login_required
@payment_required
def view_talks(request):
	registrants = UserTalkProfile.objects.filter(invited_speaker=False).values('author')
	talks = TalkSubmission.objects.filter(author__in = registrants)
        return render_to_response('talkvote/link_list.html',
            {'talks':talks,
             'paginate_by':15,
             'allow_empty':True,
             'MEDIA_URL':MEDIA_URL},
             context_instance=RequestContext(request))


@login_required
@payment_required
def vote_on_object(request, model, direction, post_vote_redirect=None,
        object_id=None, slug=None, slug_field=None, template_name=None,
        template_loader=loader, extra_context=None, context_processors=None,
        template_object_name='object', allow_xmlhttprequest=False):
    """
    Generic object vote function.

    The given template will be used to confirm the vote if this view is
    fetched using GET; vote registration will only be performed if this
    view is POSTed.

    If ``allow_xmlhttprequest`` is ``True`` and an XMLHttpRequest is
    detected by examining the ``HTTP_X_REQUESTED_WITH`` header, the
    ``xmlhttp_vote_on_object`` view will be used to process the
    request - this makes it trivial to implement voting via
    XMLHttpRequest with a fallback for users who don't have JavaScript
    enabled.

    Templates:``<app_label>/<model_name>_confirm_vote.html``
    Context:
        object
            The object being voted on.
        direction
            The type of vote which will be registered for the object.
    """
    
    if allow_xmlhttprequest and request.is_ajax():
        return xmlhttprequest_vote_on_object(request, model, direction,
                                             object_id=object_id, slug=slug,
                                             slug_field=slug_field)
    if extra_context is None: extra_context = {}
    
    

    try:
        vote = dict(VOTE_DIRECTIONS)[direction]
    except KeyError:
        raise AttributeError("'%s' is not a valid vote type." % vote_type)

    # Look up the object to be voted on
    lookup_kwargs = {}
    if object_id:
        lookup_kwargs['%s__exact' % model._meta.pk.name] = object_id
    elif slug and slug_field:
        lookup_kwargs['%s__exact' % slug_field] = slug
    else:
        raise AttributeError('Generic vote view must be called with either '
                             'object_id or slug and slug_field.')
    try:
        obj = model._default_manager.get(**lookup_kwargs)
    except ObjectDoesNotExist:
        raise Http404, 'No %s found for %s.' % (model._meta.app_label, lookup_kwargs)

    if request.method == 'POST':
        if post_vote_redirect is not None:
            next = post_vote_redirect
        elif request.REQUEST.has_key('next'):
            next = request.REQUEST['next']
        elif hasattr(obj, 'get_absolute_url'):
	    if callable(getattr(obj, 'get_absolute_url')):
                next = obj.get_absolute_url()
            else:
                next = obj.get_absolute_url
        else:
            raise AttributeError('Generic vote view must be called with either '
                                 'post_vote_redirect, a "next" parameter in '
                                 'the request, or the object being voted on '
                                 'must define a get_absolute_url method or '
                                 'property.')

	if vote != 0:
		VoteRecord.objects.record_vote(obj, request.user, vote)
	
	return HttpResponseRedirect(next)

@login_required
@payment_required
def json_error_response(error_message):
    return HttpResponse(simplejson.dumps(dict(success=False,
                                              error_message=error_message)))

@login_required
@payment_required
def xmlhttprequest_vote_on_object(request, model, direction,
    object_id=None, slug=None, slug_field=None):
    """
    Generic object vote function for use via XMLHttpRequest.

    Properties of the resulting JSON object:
        success
            ``true`` if the vote was successfully processed, ``false``
            otherwise.
        score
            The object's updated score and number of votes if the vote
            was successfully processed.
        error_message
            Contains an error message if the vote was not successfully
            processed.
    """
    if request.method == 'GET':
        return json_error_response(
            'XMLHttpRequest votes can only be made using POST.')

    UserProf = request.user.get_profile()
    if not request.user.is_authenticated():
        return json_error_response('Not authenticated.')

    try:
        vote = dict(VOTE_DIRECTIONS)[direction]
    except KeyError:
        return json_error_response(
            '\'%s\' is not a valid vote type.' % direction)
   

    # Look up the object to be voted on
    lookup_kwargs = {}
    if object_id:
        lookup_kwargs['%s__exact' % model._meta.pk.name] = object_id
    elif slug and slug_field:
        lookup_kwargs['%s__exact' % slug_field] = slug
    else:
        return json_error_response('Generic XMLHttpRequest vote view must be '
                                   'called with either object_id or slug and '
                                   'slug_field.')
    try:
        obj = model._default_manager.get(**lookup_kwargs)
    except ObjectDoesNotExist:
        return json_error_response(
            'No %s found for %s.' % (model._meta.verbose_name, lookup_kwargs))
    
    # Vote and respond
    VoteRecord.objects.record_vote(obj, request.user, vote)
    return HttpResponse(simplejson.dumps({
        'success': True,
        'score': Vote.objects.get_score(obj),
    }))
