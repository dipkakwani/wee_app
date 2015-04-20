from django import forms
from django.contrib.admin import widgets
from django.db import connection
from userModule.models import post
from groupModule.models import joins
from groupModule.models import group

"""
A post form contains a text area and a list of groups which he/she has joined. 
If the user wants to post in a group, he/she can select one of the groups from the dropdown menu.
"""
class PostForm(forms.ModelForm):
    def __init__(self, userId):
        sqlGroupId = "SELECT groupId from joins WHERE userId = %s"
        sqlGroup = "SELECT groupName, groupId from group WHERE groupId = %s"
        cursor = connection.cursor()
        cursor.execute(sqlGroupId, [userId, ])
        groupIds = cursor.fetchall()
        groups = ()
        for groupId in groupIds:
            cursor.execute(sqlGroup, [groupId, ])
            groups += cursor.fetchone()
    #TODO: Create groups menu list based on the user's joined groups.
    class Meta:
        model = post
        include = ['content', ]
