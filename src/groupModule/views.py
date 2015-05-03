from django.shortcuts import render
from groupModule.forms import GroupCreateForm
from groupModule.forms import GroupSettings
from groupModule.forms import Groups
from django.db import connection
from userModule.security import *
from django.http import HttpResponseRedirect
from django.forms.util import ErrorList

# Create your views here.
def dictFetchAll(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

def createGroup(request):
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
    #dirty query!!!make it clean
    memberssql = "SELECT j.userId_id, u.name FROM groupModule_joins j,userModule_user u WHERE j.groupId_id=%s and j.status='A' and j.userId_id=u.userId"
    cursor.execute(memberssql,[groupId ,])
    groupmembers = cursor.fetchall()
    postsql = ""
    if samegroup_check:
        #queries to be modified later
        postsql = "SELECT * from userModule_post where groupId_id=%s"      
    else:
        #queries to be modified later
        postsql = "SELECT * from userModule_post where groupId_id=%s and privacy='O'"
    cursor.execute(postsql,[groupId,])
    posts = dictFetchAll(cursor)         #make it fetch only the top few posts later
    return render(request, 'grouppage.html', {'groupname':groupname , 'posts':posts , 'members':groupmembers})

    
def groupSettings(request,groupId):
    userId = validateCookie(request)
    check_admin = "SELECT 1 FROM groupModule_group where groupId=%s and adminId_id=%s"
    cursor = connection.cursor()
    cursor.execute(check_admin,[groupId , userId ,])
    valid_group_or_person = cursor.fetchall()
    if not valid_group_or_person:
        return HttpResponseRedirect('/notfound')
    gsettings = GroupSettings(group = groupId)
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

    
def selectgroup(request):
    userId = validateCookie(request)
    if not userId:
        return HttpResponseRedirect('/home')
    selgroups = Groups(user = userId)
    if request.method == 'POST' :
        selgroups = Groups(request.POST , user = userId)
        GroupId = request.POST.get('Groups')
        return HttpResponseRedirect('/group/' + GroupId)
    return render(request, 'groupselect.html', {'groups':selgroups})