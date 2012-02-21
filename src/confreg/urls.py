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
                       url(r'^payment/$',
                           views.payment,
                           name='payment'),
                       url(r'^payment_success/(?P<slug>[^\.]+)/$',
                           views.check_wepay_success,
                           name='payment_success'),
                       url(r'^payment_fail/$',
                           views.check_wepay_fail,
                           name='payment_fail'),
                       url(r'^conf_register/$',
                           views.conf_register,
                           name='create_conf_reg'),
                       url(r'^conf_edit/$',
                           views.conf_edit,
                           name='edit_conf_reg'),
                       )
