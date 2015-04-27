#define your form here (based on the group model)
from groupModule.models import Group
from django import forms
from django.contrib.admin import widgets
from django.db import connection

class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['groupName' , 'groupType' , 'description']

#class ViewAllGroups():
    
    
    
class GroupSettings(forms.ModelForm):
    #TODO 
    #change group type
    #kick user
    #DONE
    def __init__(self, *args, **kwargs):
        groupId = kwargs.pop("group")
        super(GroupSettings, self).__init__(*args, **kwargs)
        cursor = connection.cursor()
        memberssql = "SELECT userId_id FROM groupModule_joins WHERE groupId_id=%s and status='A'"
        cursor.execute(memberssql , [groupId ,])
        GROUP_MEMBERS = cursor.fetchall()
        self.fields['removeMembers'] = forms.ChoiceField(choices=GROUP_MEMBERS)  #change to checkbox and handle the case of admin removing himself
        pendingsql = "SELECT userId_id FROM groupModule_joins WHERE status='P'"
        cursor.execute(pendingsql)
        PENDING_REQUEST = cursor.fetchall()
        self.fields['pendingRequests'] = forms.CheckboxSelectMultiple(choices = PENDING_REQUEST)
        groupTypeSql = "SELECT groupType FROM groupModule_group WHERE groupId=%s"
        cursor.execute(groupTypeSql , [groupId ,])
        GROUP_TYPE = cursor.fetchall()
        self.fields['groupType'] = forms.ChoiceField(choices=GROUP_TYPE)
        groupDescriptionsql = "SELECT description FROM groupModule_group WHERE groupId=%s"
        cursor.execute(groupDescriptionsql , [groupId ,])
        DESCRIPTION = cursor.fetchall()
        self.fields['description'] = forms.CharField(widget = forms.Textarea,initial = DESCRIPTION[0][0])
        
    class Meta:
        model = Group
    #    fields = [ 'description']
    #    widgets = {
    #            'groupType' : forms.Select() , 
    #    }