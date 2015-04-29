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
    def __init__(self, *args, **kwargs):  
        userId = kwargs.pop("user")
        super(PostForm, self).__init__(*args, **kwargs)
        groups = (('-', '-------'), )
        sqlGroup = "SELECT distinct groupId, groupName FROM groupModule_group NATURAL JOIN groupModule_joins WHERE userId_id=%s;"
        cursor = connection.cursor()
        cursor.execute(sqlGroup, [userId, ])
        groups += cursor.fetchall()
        self.fields['group'] = forms.ChoiceField(choices=groups)
    class Meta:
        model = Post
        fields = ['content', 'privacy',]

class SearchForm(forms.Form):
    queryString = forms.CharField(max_length=64)
