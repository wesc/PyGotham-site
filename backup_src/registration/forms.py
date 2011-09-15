"""
Forms and validation code for user registration.

"""

from decimal import Decimal

import settings
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required'}

NOTIFY_CHOICES = (
    ('everything', 'All things PyGotham.'),
    ('talks', 'When talk submission opens and closes, when talk voting opens and closes.'),
    ('scavenger', 'Scavenger hunt clues during the conference.'),
    ('after_party', 'Afterparties and ad-hoc social gatherings.'),
    ('after_prog', 'After-hackspace and programming contests related to this event.'),
)

PAY_CHOICES = (
    ('indiv_amt', 'I\'m registering as an individual, and will donate $100 + $3 PayPal fee.'),
    ('corp_amt', 'My company is paying, and will donate $200 + $5 PayPal fee.'),
    ('need_sponsorship', mark_safe(_("I cannot afford this fee. I need my registration sponsored,<br>and I've read <a href=\"%s/get_sponsored\">this sponsorship statement</a>." % settings.MEDIA_URL))),
    ('freebee_code', 'I have a discount code, and will enter it below.'),
)


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.
    
    """
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                required=True,
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             required=True,
                             label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                required=True,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                required=True,
                                label=_("Password (again)"))

    read_the_policy = forms.BooleanField(
		label=mark_safe(_("Yes, I've read <a href=\"%s/diversity\">this conference policy statement</a>." % settings.MEDIA_URL)),
		required=True,
		initial=False)
    
    badge_name = forms.CharField(max_length=200,min_length=60,label=_('Your full name, necessary to get into the building'))

    babysitting_request = forms.CharField(
        max_length=400,
	widget=forms.Textarea(attrs={'rows':2, 'cols':60}),
	label= mark_safe(_('Need babysitting during conference hours?<br/>Tell us the ages of your children, and any related needs')),
	initial=None)
    
    spneeds_request = forms.CharField(
        max_length=400,
	widget=forms.Textarea(attrs={'rows':2, 'cols':60}),
	label= mark_safe(_('Please list any special accomodations you may need.<br>This could be as simple as needing a reserved seat at the front of each talk/class. Read <a href=\"%s/special_needs\"> this </a>for details.' % settings.MEDIA_URL)),
	initial=None)
    

    payment_choice = forms.MultipleChoiceField(widget=forms.RadioSelect, 
        choices = PAY_CHOICES, 
	label="Payment is required to complete registration:")

    freebee_code = forms.CharField(max_length=200,min_length=60,label=_('Discount code, if applicable'))

    contact_for = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, 
        choices = NOTIFY_CHOICES, 
	label="Send me e-mail notifications related to:")

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    
    """
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms to register")})


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.
    
    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']


class RegistrationFormNoFreeEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which disallows registration with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam registrations.
    
    To change the list of banned domains, subclass this form and
    override the attribute ``bad_domains``.
    
    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com']
    
    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.
        
        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using free email addresses is prohibited. Please supply a different email address."))
        return self.cleaned_data['email']
