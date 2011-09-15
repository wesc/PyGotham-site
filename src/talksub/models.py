from django.db import models
from django.contrib.auth.models import User

Q1CHOICES = (
    ('a', 'tech talk (45 minutes)'),
    ('b', 'class (90 minutes)'),
    ('c', 'other (enter number of minutes)'))


Q3CHOICES = (
    ('a', 'beginner'),
    ('b', 'intermediate'),
    ('c', 'advanced'))


class Q3Choices(models.Model):
    answers = models.CharField(max_length=50, 
                               verbose_name="skill level",
                               choices=Q3CHOICES)
    def __unicode__(self):
        return self.answers

class TalkSubmission(models.Model):
    author = models.ForeignKey(User, unique=False, null=False, blank=False)
    accepted = models.BooleanField(default=False)    
    talktype = models.CharField(verbose_name="Talk type",
                   max_length=50,
                   choices=Q1CHOICES)
    nonstd_minutes = models.IntegerField(verbose_name="Num Minutes",
                   max_length=3,null=True,blank=True
                   )
    title = models.CharField(verbose_name="title",
                   max_length=200)
    levels = models.ManyToManyField(Q3Choices,verbose_name="levels")
    outline = models.TextField(verbose_name="outline")
    desc = models.TextField(verbose_name="desc")

    def __unicode__(self):
        return u'%s' %(self.title)

    def get_absolute_url(self):
        return "/talkvote/" #%(self.id)

    
class UserTalkProfile(models.Model):   
    """Extra data about the user that isn't normally part of models.User"""
    # This is the only required field
    author = models.ForeignKey(User,unique=True)
    invited_speaker = models.BooleanField(default=False)
    reg_notes = models.TextField(verbose_name="registration_notes")


class TalkSchedule(models.Model):   
    talk = models.ForeignKey(TalkSubmission,unique=True)
    talk_day_time = models.DateTimeField()
    room = models.CharField(verbose_name="room", max_length=50)
    duration_minutes = models.IntegerField()

