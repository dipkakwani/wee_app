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
    
    
    
class GroupSettings(forms.Form):
    #TODO 
    #change group type
    #kick user
    #DONE
    def __init__(self, *args, **kwargs):
        groupId = kwargs.pop("group")
        super(GroupSettings, self).__init__(*args, **kwargs)
        cursor = connection.cursor()
        
        GROUP_MEMBERS = (('-', '-------'), )
        memberssql = "SELECT j.userId_id, u.name FROM groupModule_joins j,userModule_user u WHERE j.groupId_id=%s and j.status='A' and j.userId_id=u.userId"
        cursor.execute(memberssql , [groupId ,])
        GROUP_MEMBERS += cursor.fetchall()
        self.fields['removeMembers'] = forms.ChoiceField(choices=GROUP_MEMBERS)  #change to checkbox and handle the case of admin removing himself
        
        PENDING_REQUEST = (('-', '-------'), )
        pendingsql = "SELECT userId_id, name FROM groupModule_joins JOIN userModule_user ON userId_id=userId WHERE groupModule_joins.status='P' and groupId_id=%s"
        cursor.execute(pendingsql , [groupId ,])
        PENDING_REQUEST += cursor.fetchall()
        self.fields['pendingRequests'] = forms.ChoiceField(choices = PENDING_REQUEST)
        
        GROUPTYPE = (('O', 'Open'), ('C', 'Closed'),)
        groupTypeSql = "SELECT groupType,CASE groupType WHEN 'O' THEN 'Open' ELSE 'Closed' END FROM groupModule_group WHERE groupId=%s"
        cursor.execute(groupTypeSql , [groupId ,])
        GROUP_TYPE = cursor.fetchone()[0].encode('ascii')
        self.fields['groupType'] = forms.ChoiceField(choices=GROUPTYPE,initial=GROUP_TYPE)
        
        groupDescriptionsql = "SELECT description FROM groupModule_group WHERE groupId=%s"
        cursor.execute(groupDescriptionsql , [groupId ,])
        DESCRIPTION = cursor.fetchall()
        self.fields['description'] = forms.CharField(widget = forms.Textarea,initial = DESCRIPTION[0][0])
        
        
        
        
class Groups(forms.Form):
    def __init__(self, *args, **kwargs):
        userId = kwargs.pop("user")
        super(Groups, self).__init__(*args, **kwargs)
        cursor = connection.cursor()
        
        groupssql = "SELECT groupId_id,groupName FROM groupModule_joins NATURAL JOIN groupModule_group WHERE groupId=groupId_id and userId_id=%s and status='A'"
        cursor.execute(groupssql , [userId,])
        GROUPS = cursor.fetchall()
        self.fields['Groups'] = forms.ChoiceField(choices = GROUPS)
