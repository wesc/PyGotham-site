from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to
from django.contrib import admin
from forms import ProfileForm
admin.autodiscover()


urlpatterns = patterns('',
    # admin urls
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    # registration search pattern

    (r'^logout/', redirect_to, {'url': '/accounts/logout/'}),
    (r'^login/', redirect_to, {'url': '/accounts/login/'}, 'login'),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^captcha/', include('captcha.urls')),
    (r'^confreg/', include('confreg.urls')),
    (r'^talksub/', include('talksub.urls')),
    (r'^talkvote/', include('talkvote.urls')),
    (r'^full_schedule/', redirect_to, {'url': '/talkvote/full_schedule/'}),
    (r'^to_be_voted_talks/', redirect_to, {'url': '/talkvote/to_be_voted_talks/'}),
    (r'^babysitting/$', direct_to_template, { 'template': 'babysitting.html' }, 'babysitting'),
    (r'^scav_hunt/$', direct_to_template, { 'template': 'scav_hunt.html' }, 'moresoon'),
    (r'^after_hack/$', direct_to_template, { 'template': 'moresoon.html' }, 'moresoon'),
    (r'^afterparty/$', direct_to_template, { 'template': 'afterparty.html' }, 'moresoon'),
    (r'^prog_contest/$', direct_to_template, { 'template': 'prog_contest.html' }, 'moresoon'),
    (r'^comingsoon/$', direct_to_template, { 'template': 'comingsoon.html' }, 'comingsoon'),
    (r'^email/', include('pygmail.urls')),
    (r'^profiles/edit', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    (r'^profiles/', include('profiles.urls')),


    (r'^$', direct_to_template, { 'template': 'home.html' }, 'home'),
    (r'^talks/$', direct_to_template, { 'template': 'talks.html' }, 'talks'),
    (r'^sponsors/$', direct_to_template, { 'template': 'sponsors.html' }, 'sponsors'),
    (r'^access/$', direct_to_template, { 'template': 'access.html' }, 'access'),
    (r'^contact_us/$', direct_to_template, { 'template': 'contact_us.html' }, 'contact_us'),
)
