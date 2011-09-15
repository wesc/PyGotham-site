from django.db import models
from django.forms import ModelForm
from django import forms
from django.shortcuts import render_to_response
from django.core import validators
from django.utils.translation import ugettext_lazy as _

 
class ProfileForm(ModelForm):
    username = forms.CharField(max_length=30) 
    email = forms.EmailField(max_length=30)


#class RegistrationForm(forms.Form):
#    username = forms.CharField(max_length=30) ##validators=[UserNameValidation])
#    email = forms.EmailField(max_length=30)
#    password1 = forms.CharField(label=_(u'Password'),widget=forms.PasswordInput(render_value=False))
#    password2 = forms.CharField(label=_(u'Password_Again'),widget=forms.PasswordInput(render_value=False))
