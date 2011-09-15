from django.contrib import admin
from confreg.models import FreeCodes,FreeCodesUsers,ConfRegModel,EmailNotifications

admin.site.register(FreeCodes)
admin.site.register(FreeCodesUsers)
admin.site.register(ConfRegModel)
admin.site.register(EmailNotifications)

