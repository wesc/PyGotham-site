from decimal import Decimal
import datetime
import random
import re

import settings
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


SHA1_RE = re.compile('^[a-f0-9]{40}$')

NOTIFY_CHOICES = (
    ('nothing', 'Send me nothing.'),
    ('everything', 'All things PyGotham.'),
    ('talks', 'When talk submission opens and closes, when talk voting opens and closes.'),
    ('scavenger', 'Scavenger hunt clues during the conference.'),
    ('after_party', 'Afterparties and ad-hoc social gatherings.'),
    ('after_prog', 'After-hackspace and programming contests related to this event.'),
)

PAY_CHOICES = (
    #('student_amt', 'I\'m registering as a student, and will pay $100 + 3% WePay fee.'),
    ('indiv_amt', 'I\'m registering as an individual, and will pay $150 + 3% WePay fee.'),
    ('corp_amt', 'My company is paying, and will pay $250 + 3% WePay fee.'),
    ('need_sponsorship', mark_safe(_("I cannot afford this fee. I need my registration sponsored,<br>and I've read <a href=\"%s/sponsors/#sponsored-content\">this sponsorship statement</a>." % settings.SSL_MEDIA_URL))),
    ('freebee_code', 'I have a registration code, and will enter it below.'),
)

class EmailNotifications(models.Model):
    notification = models.CharField(max_length=100,choices=NOTIFY_CHOICES)
    outbound_text = models.CharField(max_length=1000,null=False,blank=False)

class FreeCodesAssigned(models.Model): # One code per user. Companies get blocks of codes.
    intended_for = models.CharField(max_length=200,blank=False)
    code = models.CharField(max_length=500,unique=True,null=False,blank=False)
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'),blank=True,null=True,default=None) # filled in when used.

class ConfRegModel(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))

    read_the_policy = models.BooleanField(verbose_name=_("conf policy"),default=False)

    full_name = models.CharField(
        max_length=100, null=False,blank=False)

    babysitting = models.CharField(
        max_length=500,null=True,blank=True)

    spneeds = models.CharField(
        max_length=500,null=True,blank=True)

    payment_amount_method = models.CharField(
        max_length=50, choices = PAY_CHOICES, null=False, blank=False, default='indiv_amt')

    discount_code = models.CharField(
        max_length=100,null=True,blank=True)

    email_subjects = models.CharField(
        null=True, blank=False, max_length=100,choices=NOTIFY_CHOICES,default='everything')

    paid = models.DecimalField(max_digits=5,decimal_places=2,default=Decimal("0.00"))

    got_sponsored = models.BooleanField(verbose_name=_("got sponsorship"))

    freebee = models.BooleanField(verbose_name=_("free invited guest"))
