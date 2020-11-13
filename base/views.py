from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.

def register_view(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user_name=form.cleaned_data.get('username')
            login(request,user)
            return redirect('home')
        else:
            return render(request,'base/register.html',{'form':form})

    form=UserCreationForm()
    return render(request,'base/register.html',{'form':form})

@login_required
def home(request):
    return render(request,'base/home.html')  


def login_view(request):
    if request.method=="POST":
        form=AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            user_name=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=user_name,password=password)
            if user!=None:
                login(request,user)
                return redirect('home')
        else:
            return render(request,'base/login.html',{'form':form})
    form=AuthenticationForm() 
    return render(request,'base/login.html',{'form':form}) 

def logout_view(request):
    logout(request)
    return redirect('login')



