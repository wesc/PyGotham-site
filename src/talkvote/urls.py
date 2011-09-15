from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list

from django.conf import settings
from talksub.models import TalkSubmission,UserTalkProfile
from talkvote.views import view_talks,vote_on_object,invited_speaker_talks,\
	proposed_to_be_voted_talks,full_schedule

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$',view_talks),

	(r'^scheduled_talks/?$',invited_speaker_talks),
	#(r'^to_be_voted_talks/?$',proposed_to_be_voted_talks),
	(r'^full_schedule/?$',full_schedule),

	# Generic view to vote on Link objects
	#(r'^(?P<object_id>\d+)/(?P<direction>up|down|no_repeat|change_up|change_down)vote/$',
	#vote_on_object, dict(model=TalkSubmission, template_object_name='TalkSubmission',
	#allow_xmlhttprequest=True)),

	# View to confirm link vote
	#(r'^talk(?P<object_id>\d+)', 'talkvote.views.confirm'),

	# View to respond to repeat votes
	#(r'^one_vote', 'talkvote.views.one_vote'),
    
	# Examples:

)
