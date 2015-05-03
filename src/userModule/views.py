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
                profilePic = '/static/userModule/default.png'

                #NOTE:1.When using raw SQL Queries, you have to give the default values explicitly. 
                #     2.Always write raw sql queries as written below to escape strings and prevent SQL injection.

                sql = "INSERT INTO userModule_user (name, email, password, dob, sex, description, profilePic, school, college,\
                        companyName, status, profession, website) VALUES (%s, %s, %s, %s, %s, '', %s, '', '', '' , '', '', '')"
                cursor = connection.cursor()
                cursor.execute(sql, [name, email, h, dob, sex, profilePic, ])
                #Equivalent in Django ORM:
                #u = User(name=name, pa)sword=h, email=email,dob=d, sex=sex)
                #u.save()

                response = HttpResponseRedirect('/newsfeed')

                #Set cookie
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
def settings(request):
    form = SettingsForm()
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        #TODO:Complete this view.

def logout(request):
    response = HttpResponseRedirect('/home')
    if "sessionId" in request.COOKIES:
    	response.set_cookie('sessionId', '')
    return response