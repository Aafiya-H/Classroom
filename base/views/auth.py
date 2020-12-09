from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

from ..decorators import login_excluded
from ..forms import UserAuthenticationForm,UserRegisterationForm

from itertools import chain

@login_excluded('home')
def register_view(request):
    if request.method=="POST":
        form=UserRegisterationForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            user_name=form.cleaned_data.get('username')
            login(request,user)
            return redirect('home')
        else:
            return render(request,'base/register.html',{'form':form})
    form=UserRegisterationForm()
    return render(request,'base/register.html',{'form':form})

@login_excluded('home')  
def login_view(request):
    if request.method=="POST":
        form=UserAuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            user_name=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=user_name,password=password)
            if user!=None:
                login(request,user)
                return redirect('home')
        else:
            return render(request,'base/login.html',{'form':form})
    form=UserAuthenticationForm() 
    return render(request,'base/login.html',{'form':form}) 

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')