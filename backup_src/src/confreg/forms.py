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
        self.fields['read_the_policy'].label = mark_safe(_("Yes, I've read <a href=\"%s/diversity\">this conference policy statement</a>." % settings.SSL_MEDIA_URL))
        self.fields['full_name'].label = _('Your full name, necessary to get into the building')
        self.fields['babysitting'].label = mark_safe(_('Need babysitting during conference hours?<br/>Tell us the ages of your children, and any related needs'))
        self.fields['spneeds'].label = mark_safe(_('Please list any special accomodations you may need.<br>This could be as simple as needing a reserved seat at the front of each talk/class. Read <a href=\"%s/special_needs\"> this </a>for details.' % settings.SSL_MEDIA_URL))
        self.fields['payment_amount_method'].label = mark_safe(_('Payment is required to complete registration:'))
        self.fields['discount_code'].label = mark_safe(_('Discount code, if applicable'))
        self.fields['email_subjects'].label = mark_safe(_('Send me e-mail notifications related to:'))
        self.fields['payment_amount_method'].empty_label = None

    class Meta:
        model = ConfRegModel
        exclude = ('user','paid','got_sponsored','freebee')
        widgets = {
            'babysitting': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
            'spneeds': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
            'payment_amount_method': forms.RadioSelect(choices = PAY_CHOICES),
            #'email_subjects': forms.CheckboxSelectMultiple(choices = NOTIFY_CHOICES),
        }


'''
    read_the_policy = forms.BooleanField(
        label=mark_safe(_("Yes, I've read <a href=\"%s/diversity\">this conference policy statement</a>." % settings.SSL_MEDIA_URL)),
        required=True,
        initial=False)
    
    badge_name = forms.CharField(max_length=200,min_length=5,label=_('Your full name, necessary to get into the building'))
    
    babysitting_request = forms.CharField(
        max_length=400,
        required=False,
        initial=None,
    widget=forms.Textarea(attrs={'rows':2, 'cols':60}),
    label= mark_safe(_('Need babysitting during conference hours?<br/>Tell us the ages of your children, and any related needs')),
    )
    
    spneeds_request = forms.CharField(
        max_length=400,
        required=False,
        initial=None,
    widget=forms.Textarea(attrs={'rows':2, 'cols':60}),
    label= mark_safe(_('Please list any special accomodations you may need.<br>This could be as simple as needing a reserved seat at the front of each talk/class. Read <a href=\"%s/special_needs\"> this </a>for details.' % settings.SSL_MEDIA_URL)),
    )
    

    payment_choice = forms.ChoiceField(widget=forms.RadioSelect(choices = PAY_CHOICES), 
        choices = PAY_CHOICES, 
        required=True,
    label="Payment is required to complete registration:")

    freebee_code = forms.CharField(max_length=200,label=_('Discount code, if applicable'))

    contact_for = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, 
        choices = NOTIFY_CHOICES, 
        required=False,
        initial=None,
    label="Send me e-mail notifications related to:")
'''
