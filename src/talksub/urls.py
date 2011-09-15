from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

from talksub.views import vieweditform,add,edit

urlpatterns = patterns('',

    #TMP DEBUG:
    #url(r'^mytalks', redirect_to, {'url':'/admin/talks/talksubmission'}),
    #(r'^$', direct_to_template, { 'template': 'talks_base.html' }),

    url(r'^$', vieweditform),
    url(r'^add/?.*$', add),
    url(r'^edit/(?P<edit_id>\d+)/?$', edit),
    url(r'^edit/?.*$', redirect_to, {'url': '/'}),
                       )
