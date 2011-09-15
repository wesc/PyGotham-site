# This also imports the include function
from django.conf.urls.defaults import *

from pygmail import views

urlpatterns = patterns('',
    (r'^$', views.contact_us),
    (r'^contact_us/?.*$', views.contact_us),
)
