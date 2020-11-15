from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateClassForm(forms.Form):
    class_name = forms.CharField(max_length=100,label='class_name')
    section = forms.CharField(max_length=100,label='section')

class JoinClassForm(forms.Form):
    code = forms.CharField(max_length=10,label='code')

class UserRegisterationForm(UserCreationForm):
    password1 = forms.CharField(label='Enter password', 
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', 
                                widget=forms.PasswordInput)
 
    class Meta:
        model = User
        fields = ("username","password1","password2")
        help_texts = {
            "username":None,
        }