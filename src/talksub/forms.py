import django.forms as forms
from talksub.models import TalkSubmission, UserTalkProfile, Q1CHOICES
from django.utils.translation import ugettext_lazy as _

class TalkSubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TalkSubmissionForm, self).__init__(*args, **kwargs)
        self.fields['talktype'].label = _("What type of presentation would you like to do? Keep in mind that although company names can be mentioned occasionally, no commercial promotion is allowed:")
        self.fields['talktype'].empty_label = None
        self.fields['title'].label = _("Title of the talk/class")
        self.fields['levels'].label = _("Skill level of attendees (more than one selection is allowed)")
        self.fields['levels'].empty_label = None
        self.fields['levels'].help_text = None
        self.fields['outline'].label = _("Outline:")
        self.fields['nonstd_minutes'].label = _("Number of minutes (if \"other\"):")
        self.fields['desc'].label = _("Short Description:")

    class Meta:
        model = TalkSubmission
        exclude = ('author', 'accepted')
        widgets = {
        'outline': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        'desc': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        #'talktype': forms.RadioSelect(choices = Q1CHOICES),
        }

    def __unicode(self):
        return self.name

class UserTalkProfileForm(forms.ModelForm):
    class Meta:
        model = UserTalkProfile
        exclude = ('author','reg_notes')
    def __unicode(self):
        return self.name
