from django.contrib import admin
from confreg.models import FreeCodesAssigned,ConfRegModel,EmailNotifications

admin.site.register(FreeCodesAssigned)
admin.site.register(ConfRegModel)
admin.site.register(EmailNotifications)

