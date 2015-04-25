#define your form here (based on the group model)
from groupModule.models import Group
from django import forms
from django.contrib.admin import widgets

class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['groupName','groupType','description']

#class ViewAllGroups():
    
    
    
class GroupSettings():
    #TODO 
    #change group type
    #kick user
    class Meta:
        model = Group
