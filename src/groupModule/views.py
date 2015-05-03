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
    
def leavegroup(groupId , userId):
    cursor = connection.cursor()
    removesql = "DELETE FROM groupModule_joins WHERE groupId_id=%s and userId_id=%s"
    cursor.execute(removesql , [groupId , userId ,])
    
    checkmemberssql = "SELECT userId_id FROM groupModule_joins WHERE groupId_id=%s"
    cursor.execute(checkmemberssql , [groupId ,])
    checkMembers = cursor.fetchall()
    
    if not checkMembers:
        removecommentsql = "DELETE FROM userModule_like WHERE postId_id IN (SELECT postId FROM userModule_post WHERE groupId_id=%s)"
        cursor.execute(removecommentsql , [groupId ,])
        
        removecommentsql = "DELETE FROM userModule_share WHERE postId_id IN (SELECT postId FROM userModule_post WHERE groupId_id=%s)"
        cursor.execute(removecommentsql , [groupId ,])
        
        removecommentsql = "DELETE FROM userModule_comment WHERE postId_id IN (SELECT postId FROM userModule_post WHERE groupId_id=%s)"
        cursor.execute(removecommentsql , [groupId ,])
        
        removepostsql = "DELETE FROM userModule_post WHERE groupId_id=%s"
        cursor.execute(removepostsql , [groupId ,])
        
        removegroupsql = "DELETE FROM groupModule_group WHERE groupId=%s"
        cursor.execute(removegroupsql , [groupId ,])
    else:
        adminchecksql = "SELECT 1 FROM groupModule_group WHERE groupId=%s and adminId_id=%s"
        cursor.execute(adminchecksql , [groupId , userId ,])
        admincheck = cursor.fetchall()
        if admincheck:
            newAdmin = checkMembers[0][0]
            changeadminsql = "UPDATE groupModule_group SET adminId_id=%s WHERE groupId=%s"
            cursor.execute(changeadminsql , [newAdmin , groupId ,])

def joingroup(groupId,userId):
    cursor = connection.cursor()
    #check if user is already part of group (in case a wrong request is sent)
    checksql = "SELECT 1 FROM groupModule_joins WHERE groupId_id=%s and userId_id=%s"
    cursor.execute(checksql , [groupId , userId ,])
    checkredundancy = cursor.fetchall()
    if not checkredundancy:
        groupTypesql = "SELECT groupType FROM groupModule_group WHERE groupId=%s"
        cursor.execute(groupTypesql , [groupId ,])
        groupType = cursor.fetchall()
        if groupType[0][0] == 'O' :
            joinsql = "INSERT INTO groupModule_joins (groupId_id,userId_id,status) VALUES (%s,%s,%s)"
            cursor.execute(joinsql , [groupId,userId,'A'])
        else:
            joinsql = "INSERT INTO groupModule_joins (groupId_id,userId_id,status) VALUES (%s,%s,%s)"
            cursor.execute(joinsql , [groupId,userId,'P'])
    
def group(request,groupId):
    userId = validateCookie(request)
    groupsql = "SELECT groupName FROM groupModule_group where groupId=%s"
    cursor = connection.cursor()
    cursor.execute(groupsql,[groupId ,])
    groupexists = cursor.fetchall()
    
    if not groupexists:
        return HttpResponseRedirect('/notfound')
    
    if request.method == 'POST':
        if 'LeaveGroup' in request.POST:
            leavegroup(groupId,userId)
            return render(request , 'leaveGroup.html')
        elif 'JoinGroup' in request.POST:
            joingroup(groupId,userId)
            return HttpResponseRedirect('/group/'+str(groupId))
    
    groupname = groupexists[0][0]  #the tuple containing group name
    group_checksql = "SELECT 1 FROM groupModule_joins where groupId_id=%s and userId_id=%s and status='A'"
    cursor.execute(group_checksql,[groupId , userId ,])
    samegroup_check = cursor.fetchall()
    
    #dirty query!!!make it clean
    memberssql = "SELECT j.userId_id, u.name FROM groupModule_joins j,userModule_user u WHERE j.groupId_id=%s and j.status='A' and j.userId_id=u.userId"
    cursor.execute(memberssql,[groupId ,])
    groupmembers = dictFetchAll(cursor)
    
    postsql = ""
    if samegroup_check:
        #queries to be modified later
        postsql = "SELECT * FROM userModule_post JOIN userModule_user ON posterId_id=userId WHERE groupId_id=%s"      
    else:
        #queries to be modified later
        postsql = "SELECT * FROM userModule_post JOIN userModule_user ON posterId_id=userId WHERE groupId_id=%s and privacy='P'"
    cursor.execute(postsql,[groupId,])
    posts = dictFetchAll(cursor)       #make it fetch only the top few posts later
    
    check_admin = "SELECT DISTINCT groupId FROM groupModule_group where groupId=%s and adminId_id=%s" #selecting groupid to reduce 1 more field to be sent to html
    cursor.execute(check_admin,[groupId , userId ,])
    adminCheck_with_id = cursor.fetchall()
    if adminCheck_with_id:
        adminCheck_with_id=adminCheck_with_id[0][0]
    
    descriptionsql = "SELECT description FROM groupModule_group WHERE groupId=%s"""
    cursor.execute(descriptionsql , [groupId ,])
    description = cursor.fetchall()[0][0]
    return render(request, 'grouppage.html', {'groupname':groupname , 'posts':posts , 'members':groupmembers , 'samegroup':samegroup_check ,
                                                                'admin':adminCheck_with_id , 'description':description})

    
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
            acceptRequestSql = "UPDATE groupModule_joins SET status='A' where userId_id IN (%s) and groupId_id=%s"
            userlist = ""
            flag = True
            for user in pendingRequests:
                if flag==True:
                    userlist +=user
                    flag = False
                    continue
                userlist +=",'%s'"%(user , )
            cursor.execute(acceptRequestSql , [userlist , groupId ,])
            
            if deleteMember == userId:
                errors = gsettings._error.setdefault('removeMembers' , ErrorList())
                errors.append(u"You cannot remove yourself from the group")
            deletesql = "DELETE FROM groupModule_joins WHERE userId_id=%s and groupId_id=%s"
            cursor.execute(deletesql , [deleteMember , groupId ,])
            groupEditsql = "UPDATE groupModule_group SET groupType=%s , description=%s where groupId=%s"
            cursor.execute(groupEditsql , [groupType , description , groupId ,])
            return HttpResponseRedirect('/group/%s/settings/'%(groupId))
    return render(request, 'groupsettings.html', {'groupsettings':gsettings})

    
def selectgroup(request):
    userId = validateCookie(request)
    if not userId:
        return HttpResponseRedirect('/home')
    selgroups = Groups(user = userId)
    if request.method == 'POST' :
        selgroups = Groups(request.POST , user = userId)
        if selgroups.is_valid():
            GroupId = request.POST.get('Groups')
            return HttpResponseRedirect('/group/' + GroupId)
    return render(request, 'groupselect.html', {'groups':selgroups})
 
 
