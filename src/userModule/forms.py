from userModule.models import User
from django import forms
from django.db import connection
from django.contrib.admin import widgets
from wee.views import dictFetchAll

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'dob', 'password','sex', ]
        widgets = {
            'password' : forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=40)
    password = forms.CharField(max_length=70, widget=forms.PasswordInput())

class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['userId', 'email', ]
        widgets = {
                'password' : forms.PasswordInput(),
        }
