from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from confreg import views


urlpatterns = patterns('',
                       url(r'^/$',
                           views.user_state,
                           name='check_user_state'),
                       url(r'^user_state/$',
                           views.user_state,
                           name='check_user_state'),
                       (r'^need_to_activate/?$', direct_to_template, { 'template': 'confreg/need_to_activate.html' }, 'need_to_activate'),
                       url(r'^conf_register/$',
                           views.conf_register,
                           name='create_conf_reg'),
                       )
