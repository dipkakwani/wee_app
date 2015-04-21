from django import forms
from django.contrib.admin import widgets
from django.db import connection
from userModule.models import Post
from groupModule.models import Joins
from groupModule.models import Group

"""
A post form contains a text area, privacy type and a list of groups which he/she has joined. 
If the user wants to post in a group, he/she can select one of the groups from the dropdown menu.
"""
class PostForm(forms.ModelForm):
    def __init__(self, userId, *args, **kwargs):  
        super(PostForm, self).__init__(*args, **kwargs)

        sqlGroupId = "SELECT groupId_id from groupModule_joins WHERE userId_id = %s"
        sqlGroup = "SELECT groupId, groupName from groupModule_group WHERE groupId = %s"
        cursor = connection.cursor()
        cursor.execute(sqlGroupId, [userId, ])
        groupIds = cursor.fetchall()
        groups = ()
        for groupId in groupIds:
            cursor.execute(sqlGroup, [groupId, ])
            groups += cursor.fetchone()
        self.fields['group'] = forms.ChoiceField(choices=groups)
    class Meta:
        model = Post
        fields = ['content', 'privacy',]
