from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

from talkvote.managers import VoteManager

SCORES = (
    (u'+1', +1),
    (u'-1', -1),
)

MODES = (
	('not_started', 'not_started'),
	('active', 'active'),
	('ended', 'ended')
)

class VotingVars(models.Model):
	voting_mode = models.CharField(max_length=15,choices=MODES)

	def __unicode__(self):
		return u'%s' %(self.voting_mode)


class VoteRecord(models.Model):
	user = models.ForeignKey(User)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
    	object = generic.GenericForeignKey('content_type', 'object_id')
    	vote = models.SmallIntegerField(choices=SCORES)
	
	objects = VoteManager()

        class Meta:
        	db_table = 'votes'
        	# One vote per user per object
        	unique_together = (('user', 'content_type', 'object_id'),)

    	def __unicode__(self):
        	return u'%s: %s on %s' % (self.user, self.vote, self.object)

        def is_upvote(self):
        	return self.vote == 1

        def is_downvote(self):
        	return self.vote == -1

	def has_voted(self):
        	return self.vote != 0

