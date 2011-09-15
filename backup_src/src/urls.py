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
    (r'^login/', redirect_to, {'url': '/accounts/login/'}),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^captcha/', include('captcha.urls')),
    (r'^confreg/', include('confreg.urls')),
    #(r'^accounts/', include(registration.urls)),
    (r'^$', direct_to_template, { 'template': 'slideshow.html' }, 'slideshow'),
    (r'^special_needs/?$', direct_to_template, { 'template': 'spneeds.html' }, 'spneeds'),
    (r'^babysitting/?$', direct_to_template, { 'template': 'babysitting.html' }, 'babysitting'),
    (r'^diversity/?$', direct_to_template, { 'template': 'diversity.html' }, 'diversity'),
    (r'^talks/?.*$', direct_to_template, { 'template': 'talks.html' }, 'talks'),
    (r'^howto_sponsor/?.*$', direct_to_template, { 'template': 'be_a_sponsor.html' }, 'be_a_sponsor'),
    (r'^get_sponsored/?.*$', direct_to_template, { 'template': 'be_sponsored.html' }, 'be_sponsored'),
    (r'^scav_hunt/?.*$', direct_to_template, { 'template': 'moresoon.html' }, 'moresoon'),
    (r'^contact_us/?.*$', direct_to_template, { 'template': 'contact_us.html' }, 'contact_us'),
    (r'^after_hack/?.*$', direct_to_template, { 'template': 'moresoon.html' }, 'moresoon'),
    (r'^afterparty/?.*$', direct_to_template, { 'template': 'moresoon.html' }, 'moresoon'),
    (r'^prog_contest/?.*$', direct_to_template, { 'template': 'moresoon.html' }, 'moresoon'),
    (r'^comingsoon/?.*$', direct_to_template, { 'template': 'comingsoon.html' }, 'comingsoon'),
    (r'^email/', include('pygmail.urls')),
    (r'^profiles/edit', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    (r'^profiles/', include('profiles.urls')),

)
