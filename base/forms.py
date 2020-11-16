from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from . import models
import datetime

class CreateClassForm(forms.Form):
    class_name = forms.CharField(max_length=100,label='class_name')
    section = forms.CharField(max_length=100,label='section')

class JoinClassForm(forms.Form):
    code = forms.CharField(max_length=10,label='code')

class CreateAssignmentForm(forms.Form):
    assignment_name = forms.CharField(max_length=50,label='assignment_name')
    due_date = forms.DateField(initial=datetime.date.today(),label='due_date')
    instructions = forms.CharField(label='class_name',widget=forms.Textarea)
    total_marks = forms.IntegerField(label='total_marks')

class UserRegisterationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-enter Password'


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

class UserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


    password = forms.CharField(label='Enter password', 
                                widget=forms.PasswordInput)
 
    class Meta:
        model = User
        fields = ("username","password")
        help_texts = {
            "username":None,
        }
