from userModule.models import User
from django import forms
from django.contrib.admin import widgets
class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['userId', 'description', 'profilePic', 'school', 'college', 'companyName' ,'status', 'profession', 'website', ]
        widgets = {
            'password' : forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=40)
    password = forms.CharField(max_length=70, widget=forms.PasswordInput())

class SettingsForm(forms.ModelForm):
    #TODO: Make each field optional.
    class Meta:
        model = User
        exclude = ['userId', 'email']
        widgets = {
                'password' : forms.PasswordInput(),
        }
