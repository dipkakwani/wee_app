"""
Author : Diptanshu Kakwani
"""
from django.db import models
from datetime import datetime

"""
An open group can be joined by anyone whereas, in case of a closed group a confirmation is required from the admin.
"""
class Group(models.Model):
   groupId = models.AutoField(primary_key=True)
   groupName = models.CharField(max_length=64)
   GROUPTYPE = (('O', 'Open'), ('C', 'Closed'),)
   groupType = models.CharField(max_length=1, choices=GROUPTYPE)
   description = models.TextField()
   adminId = models.ForeignKey('userModule.User')

"""
User -- Joins -- Group
A many-to-many relationship between User and Group
"""
class Joins(models.Model):
    groupId = models.ForeignKey('Group')
    userId = models.ForeignKey('userModule.User')
    STATUS = (('P','Pending') , ('A' , 'Accepted'), )
    status = models.CharField(max_length=1 , choices=STATUS)
    class Meta:
        unique_together = (('groupId'), ('userId'),)
