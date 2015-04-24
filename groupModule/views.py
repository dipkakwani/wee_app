from django.shortcuts import render
from groupModule.forms import GroupCreateForm
from django.db import connection
from userModule.security import *
from django.http import HttpResponseRedirect

# Create your views here.
def createGroup(request):
    #TODO: Define a view to create a group
    #start with forms.py and the html file
    #take help from userModule/forms.py and userModule/template/home.html and userModule/views.py
    #remove these comments...
    userId=validateCookie(request)
    if not userId:
        return HttpResponseRedirect('/home/')
    creategroup = GroupCreateForm(request.POST)
    if request.method == 'POST':
        if creategroup.is_valid():
            name = request.POST.get('name')
            gname = request.POST.get('groupName')
            gtype = request.POST.get('groupType')
            
            sql = "INSERT INTO groupmodule_group (groupName , groupType , adminId_id) VALUES (%s , %s , %s)"
            
            cursor = connection.cursor()
            cursor.execute(sql, [gname , gtype ,userId,])
            groupid = cursor.lastrowid
            return HttpResponseRedirect('/group/'+groupid)
            #return HttpResponseRedirect('/group/')
            
    return render(request, 'creategroup.html', {'GroupCreateForm' : creategroup,})
    
    
def group(request,groupid):
    #TODO
    #display group posts
    userid=validateCookie(request)