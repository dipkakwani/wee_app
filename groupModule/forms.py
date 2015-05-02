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
        
        memberssql = "SELECT j.userId_id, u.name FROM groupModule_joins j,userModule_user u WHERE j.groupId_id=%s and j.status='A' and j.userId_id=u.userId"
        cursor.execute(memberssql , [groupId ,])
        GROUP_MEMBERS = cursor.fetchall()
        self.fields['removeMembers'] = forms.ChoiceField(choices=GROUP_MEMBERS)  #change to checkbox and handle the case of admin removing himself
        
        pendingsql = "SELECT userId_id, name FROM groupModule_joins NATURAL JOIN userModule_user WHERE status='P'"
        cursor.execute(pendingsql)
        PENDING_REQUEST = cursor.fetchall()
        self.fields['pendingRequests'] = forms.ChoiceField(choices = PENDING_REQUEST)
        
        GROUPTYPE = (('O', 'Open'), ('C', 'Closed'),)
        groupTypeSql = "SELECT groupType FROM groupModule_group WHERE groupId=%s"
        cursor.execute(groupTypeSql , [groupId ,])
        GROUP_TYPE = cursor.fetchall()
        self.fields['groupType'] = forms.ChoiceField(choices=GROUPTYPE,initial=GROUP_TYPE)
        
        groupDescriptionsql = "SELECT description FROM groupModule_group WHERE groupId=%s"
        cursor.execute(groupDescriptionsql , [groupId ,])
        DESCRIPTION = cursor.fetchall()
        self.fields['description'] = forms.CharField(widget = forms.Textarea,initial = DESCRIPTION[0][0])
        
    class Meta:
        model = Group
        fields = []
        widget = {
                
        }
        
        
        
class Groups(forms.Form):
    def __init__(self, *args, **kwargs):
        userId = kwargs.pop("user")
        super(Groups, self).__init__(*args, **kwargs)
        cursor = connection.cursor()
        
        groupssql = "SELECT groupId_id,groupName FROM groupModule_joins NATURAL JOIN groupModule_group WHERE groupId=groupId_id and userId_id=%s"
        cursor.execute(groupssql , [userId,])
        GROUPS = cursor.fetchall()
        self.fields['Groups'] = forms.ChoiceField(choices = GROUPS)
