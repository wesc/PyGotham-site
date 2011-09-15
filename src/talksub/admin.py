from django.contrib import admin

from talksub.models import *


admin.site.register(TalkSubmission)
admin.site.register(UserTalkProfile)
admin.site.register(TalkSchedule)

