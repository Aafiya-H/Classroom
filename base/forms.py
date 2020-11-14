from django import forms

class CreateClassForm(forms.Form):
    class_name = forms.CharField(max_length=100,label='class_name')
    section = forms.CharField(max_length=100,label='section')

class JoinClassForm(forms.Form):
    code = forms.CharField(max_length=10,label='code')