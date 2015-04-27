from django.shortcuts import render
from groupModule.forms import GroupCreateForm
from groupModule.forms import GroupSettings
from django.db import connection
from userModule.security import *
from django.http import HttpResponseRedirect
from django.forms.util import ErrorList

# Create your views here.
def createGroup(request):
    #TODO: Define a view to create a group
    #start with forms.py and the html file
    #take help from userModule/forms.py and userModule/template/home.html and userModule/views.py
    #remove these comments...
    userId=validateCookie(request)
    if not userId:
        return HttpResponseRedirect('/home/')
    creategroup = GroupCreateForm()
    if request.method == 'POST':
        creategroup = GroupCreateForm(request.POST)
        if creategroup.is_valid():
#            name = request.POST.get('name')
            gname = request.POST.get('groupName')
            gtype = request.POST.get('groupType')
            gdesc = request.POST.get('description')
            
            sql1 = "INSERT INTO groupModule_group (groupName , groupType , adminId_id , description) VALUES (%s , %s , %s , %s)"
            sql2 = "INSERT INTO groupModule_joins (groupId_id,userId_id,status) VALUES (%s,%s,%s)"
            
            cursor = connection.cursor()
            cursor.execute(sql1, [gname , gtype , userId , gdesc ,])
            groupId = cursor.lastrowid
            cursor.execute(sql2,[groupId,userId,'A'])
            return HttpResponseRedirect('/group/'+str(groupId))
            
    return render(request, 'creategroup.html', {'GroupCreateForm' : creategroup,})
    
    
def group(request,groupId):
    userId = validateCookie(request)
    groupsql = "SELECT groupName FROM groupModule_group where groupId=%s"
    cursor = connection.cursor()
    cursor.execute(groupsql,[groupId ,])
    groupexists = cursor.fetchall()
    if not groupexists:
        return HttpResponseRedirect('/notfound')
    groupname = groupexists[0][0]  #the tuple containing group name
    group_checksql = "SELECT 1 FROM groupModule_joins where groupId_id=%s and userId_id=%s"
    cursor.execute(group_checksql,[groupId , userId ,])
    samegroup_check = cursor.fetchall()
    memberssql = "SELECT userId_id FROM groupModule_joins where groupId_id=%s"
    cursor.execute(memberssql,[groupId ,])
    groupmembers = cursor.fetchall()
    postsql = ""
    if samegroup_check:
        #queries to be modified later
        postsql = "SELECT postId,time,likes,comments,shares,content,posterId_id from userModule_post where groupId_id=%s"      
    else:
        #queries to be modified later
        postsql = "SELECT postId,time,likes,comments,shares,content,posterId_id from userModule_post where groupId_id=%s and privacy='O'"
    cursor.execute(postsql,[groupId,])
    posts = cursor.fetchall()         #make it fetch only the top few posts later
    return render(request, 'grouppage.html', {'groupname':groupname , 'posts':posts , 'members':groupmembers})

    
def groupSettings(request,groupId):
    userId = validateCookie(request)
    check_admin = "SELECT 1 FROM groupModule_group where groupId=%s and adminId_id=%s"
    cursor = connection.cursor()
    cursor.execute(check_admin,[groupId , userId ,])
    valid_group_or_person = cursor.fetchall()
    if not valid_group_or_person:
        return HttpResponseRedirect('/notfound')
    gsettings = GroupSettings(group=groupId)
    if request.method == 'POST' :
        gsettings = GroupSettings(request.POST , group=groupId)
        if gsettings.is_valid():
            deleteMember = request.POST.get('removeMembers')
            groupType = request.POST.get('groupType')
            description = request.POST.get('description')
            pendingRequests = request.POST.get('pendingRequests')
            acceptRequestSql = "UPDATE groupModule_joins SET status='A' where userId_id IN (%s)"
            userlist = ""
            flag = True
            for user in pendingRequest:
                if flag==True:
                    userlist.append(user)
                    flag = False
                    continue
                userlist.append(",'%s'"%(user , ))
            cursor.execute(acceptRequestSql , [userlist , ])
            
            if deleteMember == userId:
                errors = gsettings._error.setdefault('removeMembers' , ErrorList())
                errors.append(u"You cannot remove yourself from the group")
            deletesql = "DELETE FROM groupModule_joins WHERE userId_id=%s"
            cursor.execute(deletesql , [deleteMember , ])
            groupEditsql = "UPDATE groupModule_group SET groupType=%s and description=%s where groupId=%s"
            cursor.execute(groupEditsql , [groupType , description , groupId ,])
            return HttpResponseRedirect('/group/%s/settings'%(groupId))
    return render(request, 'groupsettings.html', {'groupsettings':gsettings})