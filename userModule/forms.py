from userModule.models import User
from django import forms
from django.contrib.admin import widgets
class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'dob', 'password','sex', ]
        widgets = {
            'password' : forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    class Meta:
        model = User
        fields = ['email', 'password', ]
        widgets = {
                'password' : forms.PasswordInput()
        }
        
class SettingsForm(forms.ModelForm):
    #TODO: Make each field optional.
    class Meta:
        model = User
        exclude = ['userId', 'email']
        widgets = {
                'password' : forms.PasswordInput(),
        }
