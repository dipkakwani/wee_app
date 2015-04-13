"""
Author : Diptanshu Kakwani
"""
from django.db import models
from datetime import datetime

class Group(models.Model):
   groupId = models.AutoField(primary_key=True)
   groupName = models.CharField(max_length=64)
   adminId = models.ForeignKey('userModule.User')

"""
User -- Joined -- Group
A many-to-many relationship between User and Group
"""
class Joined(models.Model):
    groupId = models.ForeignKey('Group')
    userId = models.ForeignKey('userModule.User')

"""
User posts something.
The post may or may not belong to a Group.
"""
class Post(models.Model):
    postId = models.AutoField(primary_key=True)
    posterId = models.ForeignKey('userModule.User')
    PRIVACY = (('L','Limited'), ('P', 'Public'),)
    privacy = models.CharField(max_length=1, choices=PRIVACY)
    time = models.DateTimeField(default=datetime.now)
    likes = models.BigIntegerField(default=0)
    comments = models.BigIntegerField(default=0)
    shares = models.BigIntegerField(default=0)
    content = models.TextField()
    groupId = models.ForeignKey('Group', null=True)
    class Meta:
        ordering = ['-time']
