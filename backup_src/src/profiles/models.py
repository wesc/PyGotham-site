from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # This is the only required field
    #user = models.ForeignKey(User, unique=True)
    user = models.ForeignKey(User, unique=True)
    address = models.CharField(max_length=50)
    system_state = models.IntegerField()
    def __unicode__(self):
        return '%s' % self.user
