from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
import datetime

class CreateClassForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(CreateClassForm,self).__init__()
        self.fields['class_name'].label=''
        self.fields['section'].label=''
        self.fields['class_name'].widget.attrs['placeholder']='Class Name'
        self.fields['section'].widget.attrs['placeholder']='Section'
    
    class_name = forms.CharField(max_length=100,label='Class name')
    section = forms.CharField(max_length=100,label='Section')

class JoinClassForm(forms.Form):
    code = forms.CharField(max_length=10,label='code')

class CreateAssignmentForm(forms.Form):
    assignment_name = forms.CharField(max_length=50,label='Assignment Name')
    due_date = forms.DateField(initial=datetime.date.today(),label='Due Date')
    due_time = forms.TimeField(initial=datetime.time(10,10),label='Due Time')
    instructions = forms.CharField(label='Instructions',widget=forms.Textarea)
    total_marks = forms.IntegerField(label='Total Marks')

class SubmitAssignmentForm(forms.Form):
    submission_file = forms.FileField()

class UserRegisterationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['profile_photo'].label = ''
        self.fields['profile_photo'].widget.attrs['placeholder'] = 'Profile photo'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-enter Password'

    password1 = forms.CharField(label='Enter password', 
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', 
                                widget=forms.PasswordInput)
 
    class Meta:
        model = CustomUser
        fields = ("username","password1","password2",'email','profile_photo')
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
        model = CustomUser
        fields = ("username","password")
        help_texts = {
            "username":None,
        }
