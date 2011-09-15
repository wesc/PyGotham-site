# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from settings import TALK_SUBMISSION_LIMIT_PER_PERSON,TALK_STATE,\
	SSL_MEDIA_URL, MEDIA_URL
from talksub.forms import TalkSubmissionForm, UserTalkProfileForm
from talksub.models import TalkSubmission, UserTalkProfile
from confreg.views import payment_required


@login_required
@payment_required
def add(request):
    return vieweditform(request,add=True)

@login_required
@payment_required
def edit(request,edit_id):
    return vieweditform(request,add=False,edit_id=edit_id)

@login_required
@payment_required
def vieweditform(request,add=False,edit_id=None):
    """Talk Submission: enable users to edit existing or create new talks"""

    # Create this here as well, since it was introduced late in the code.
    #talk_profile = UserTalkProfile.objects.get(author=request.user)
    talk_profile,created = UserTalkProfile.objects.get_or_create(author=request.user)

    try:
        talks = TalkSubmission.objects.filter(author=request.user)
        howmany = talks.count()
    except TalkSubmission.DoesNotExist:
        talks = None
        howmany = 0

    msg = None
    if talk_profile.invited_speaker:
        msg = mark_safe("As an Invited Speaker, no one can vote on your talk,<br> but you will be able to vote on other people's talks.")
    elif howmany >= TALK_SUBMISSION_LIMIT_PER_PERSON:
        msg = "You've already entered three talks, and can only modify existing talks."

    #if editing a previously submitted talk, re-create form from db
    if request.method != 'POST':
        if add:
            if howmany >= TALK_SUBMISSION_LIMIT_PER_PERSON:
                return render_to_response('talksub/mytalks.html', 
                    {'form': None,
                     'talks':talks,
                     'edit_id':edit_id,
                     'generic_error':msg,
                     'MEDIA_URL':MEDIA_URL,
                     'addtalks':howmany < TALK_SUBMISSION_LIMIT_PER_PERSON},
                     context_instance=RequestContext(request))

            form = TalkSubmissionForm() 
	elif edit_id:
            try:
                talksubm = TalkSubmission.objects.get(author=request.user,id=edit_id)
            except TalkSubmission.DoesNotExist:
                # Hacking, just send them back.
                return redirect(MEDIA_URL) 
            
            form = TalkSubmissionForm(instance=talksubm)
        else:
            form = None
        return render_to_response('talksub/mytalks.html', 
            {'form': form, 
             'talks':talks,
             'edit_id':edit_id,
             'generic_error':msg,
             'MEDIA_URL':MEDIA_URL,
             'addtalks':howmany < TALK_SUBMISSION_LIMIT_PER_PERSON},
             context_instance=RequestContext(request))

    # If not editing your talk, create a new talk & update TalkSubmission
    else:
        if not edit_id and howmany >= TALK_SUBMISSION_LIMIT_PER_PERSON:
            return render_to_response('talksub/mytalks.html', 
                 {'form': None,
                  'talks':talks,
                  'edit_id':None,
                  'generic_error':msg,
                  'MEDIA_URL':MEDIA_URL,
                  'addtalks':howmany < TALK_SUBMISSION_LIMIT_PER_PERSON},
                  context_instance=None)

        form = TalkSubmissionForm(request.POST)
        if form.is_valid():
            if add:
                talksubm = TalkSubmission.objects.create(author=request.user)
            else:
                talksubm = TalkSubmission.objects.get(author=request.user,id=edit_id)

            newform = TalkSubmissionForm(request.POST,instance=talksubm)
            newform.save()
            form = None

            return redirect(MEDIA_URL + '/talksub/')

        else:
            return render_to_response('talksub/mytalks.html', 
                 {'form': form,
                  'talks':talks,
                  'edit_id':None,
                  'generic_error':msg,
                  'MEDIA_URL':MEDIA_URL,
                  'addtalks':howmany < TALK_SUBMISSION_LIMIT_PER_PERSON},
                  context_instance=None)

