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
User -- Joins -- Group
A many-to-many relationship between User and Group
"""
class Join(models.Model):
    groupId = models.ForeignKey('Group')
    userId = models.ForeignKey('userModule.User')
    class Meta:
        unique_together = (('groupId'), ('userId'),)
