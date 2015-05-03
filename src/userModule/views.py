"""
Author : Diptanshu Kakwani
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.db import connection
from userModule.forms import SignupForm
from userModule.forms import LoginForm
from userModule.forms import SettingsForm
from django.forms.util import ErrorList
from userModule.models import User
from wee.views import dictFetchOne
from django.conf import settings

from security import *
import os

#Cobmined signup and login view
def home(request):
    # Is the user already logged in
    if validateCookie(request):
	    return HttpResponseRedirect('/newsfeed')

    signup = SignupForm()
    login = LoginForm()
    if request.method == 'POST':
        if 'submitSignup' in request.POST:       #Signup form submitted
            signup = SignupForm(request.POST)
            if signup.is_valid():
                name = request.POST.get('name')
                password = request.POST.get('password')
                email = request.POST.get('email')
                dob = request.POST.get('dob')
                sex = request.POST.get('sex')
                h = hashPassword(name, password)

                #NOTE:1.When using raw SQL Queries, you have to give the default values explicitly.
                #     2.Always write raw sql queries as written below to escape strings and prevent SQL injection.

                sql = "INSERT INTO userModule_user (name, email, password, dob, sex, description, profilePic, school, college,\
                        companyName, status, profession, website) VALUES (%s, %s, %s, %s, %s, '', %s, '', '', '' , '', '', '')"
                cursor = connection.cursor()
                cursor.execute(sql, [name, email, h, dob, sex, profilePic, ])
                #Equivalent in Django ORM:
                #u = User(name=name, password=h, email=email,dob=d, sex=sex)
                #u.save()

                response = HttpResponseRedirect('/newsfeed')

                #Set cookie"
                setCookie(response, h)

                return response

        elif 'submitLogin' in request.POST:     #Login form submitted
            login = LoginForm(request.POST)
            if login.is_valid():
                email = request.POST.get('email')
                pw = request.POST.get('password')
                cursor = connection.cursor()
                sql = "SELECT name, password from userModule_user WHERE email=%s"
                cursor.execute(sql, [email, ])
                row = cursor.fetchone()
                if row and validPassword(row[0], pw, row[1]):
                    response = HttpResponseRedirect('/newsfeed')
		    setCookie(response, row[1])
                    return response

                else:
                    errors = login._errors.setdefault("password", ErrorList())
                    errors.append(u"Invalid email or password")
    return render(request, 'home.html', {'loginForm' : login, 'signupForm' : signup})

#To change the settings/preferences of the user.
def userSettings(request):
    userId = validateCookie(request)
    if not userId:
        return HttpResponseRedirect("/home")

    cursor = connection.cursor()
    # Fetch current values for the corresponding userId
    userInfoSql = "SELECT name, dob, sex, description, profilePic, school, college, companyName, status, profession, website FROM userModule_user\
                      WHERE userId=%s"
    cursor.execute(userInfoSql, [userId, ])
    userInfo = dictFetchOne(cursor)

    form = SettingsForm(initial=userInfo)
    if request.method == 'POST':
        print "Got post request"
        form = SettingsForm(request.POST, request.FILES, initial=userInfo)
        if form.is_valid():
            name = request.POST.get('name')
            dob = request.POST.get('dob')
            sex = request.POST.get('sex')
            description = request.POST.get('description')
            profilePic = str(userId) + "." + request.FILES['profilePic'].name\
                        if request.FILES['profilePic'].name else settings.defaultProfilePic
            school = request.POST.get('school')
            college = request.POST.get('college')
            companyName = request.POST.get('companyName')
            status = request.POST.get('status')
            profession = request.POST.get('profession')
            website = request.POST.get('website')
            print "Got profile picture " + request.FILES['profilePic'].name
            updateSql = "UPDATE userModule_user SET name=%s, dob=%s, sex=%s, description=%s, profilePic=%s, school=%s,\
                         college=%s, companyName=%s, status=%s, profession=%s, website=%s WHERE userId=%s"
            if request.FILES['profilePic']:
                saveFile(request.FILES['profilePic'], settings.MEDIA_ROOT + str(userId) + "." + request.FILES['profilePic'].name)
            cursor.execute(updateSql, [name, dob, sex, description, profilePic, school, college, companyName,\
                                       status, profession, website, userId, ])

    return render(request, 'settings.html', {'form' : form, 'userId' : userId, })

def logout(request):
    response = HttpResponseRedirect('/home')
    if "sessionId" in request.COOKIES:
    	response.set_cookie('sessionId', '')
    return response

def saveFile(fileContent, destinationFileName):
    print "Saving file to destination " + destinationFileName
    with open(destinationFileName, "wb+") as destinationFile:
        for chunk in fileContent.chunks():
            destinationFile.write(chunk)
