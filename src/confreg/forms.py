"""
Forms and validation code for conference registration.

"""

from decimal import Decimal

import settings
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from confreg.models import ConfRegModel,NOTIFY_CHOICES,PAY_CHOICES
from captcha.fields import CaptchaField


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required'}

class ConfRegForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConfRegForm, self).__init__(*args, **kwargs)
        self.fields['read_the_policy'].label = mark_safe(_("Yes, I've read <a class=\"selected\" href=\"%s/access/#diversity-content\">this conference policy statement</a>." % settings.SSL_MEDIA_URL))
        self.fields['full_name'].label = _('Your full name, necessary to get into the facility')
        self.fields['babysitting'].label = mark_safe(_('Need babysitting during conference hours?<br/>Tell us the ages of your children, and any related needs'))
        self.fields['assistance'].label = mark_safe(_('Please list any accessibility accomodations you may need.<br>This could be as simple as needing a reserved seat at the front of each talk/class. Read <a href=\"%s/access/#accessibility-content\"> this </a>for details.' % settings.SSL_MEDIA_URL))
        self.fields['payment_amount_method'].label = mark_safe(_('Payment is required to complete registration:'))
        self.fields['discount_code'].label = mark_safe(_('Registration code, if you have one'))
        self.fields['email_subjects'].label = mark_safe(_('Send me e-mail notifications related to:'))
        self.fields['payment_amount_method'].empty_label = None

    class Meta:
        model = ConfRegModel
        exclude = ('user')
        widgets = {
            'babysitting': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
            'assistance': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
            'payment_amount_method': forms.RadioSelect(choices = PAY_CHOICES),
            #'email_subjects': forms.CheckboxSelectMultiple(choices = NOTIFY_CHOICES),
        }
