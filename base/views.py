from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CreateClassForm,UserRegisterationForm, UserAuthenticationForm
from .utils import generate_class_code
from .models import Classrooms,Teachers,Students
from .forms import JoinClassForm

from itertools import chain

def register_view(request):
    if request.method=="POST":
        form=UserRegisterationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user_name=form.cleaned_data.get('username')
            login(request,user)
            return redirect('home')
        else:
            return render(request,'base/register.html',{'form':form})
    form=UserRegisterationForm()
    return render(request,'base/register.html',{'form':form})

def home(request):
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping) 
    return render(request,'base/home.html',{'mappings':mappings})  

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

def logout_view(request):
    logout(request)
    return redirect('login')

def create_class(request):
    if request.method == 'POST':
        form = CreateClassForm(request.POST)
        if form.is_valid():
            class_name = form.cleaned_data.get('class_name')
            section = form.cleaned_data.get('section')
            class_code = generate_class_code(6)
            classroom = Classrooms(classroom_name=class_name,section=section,class_code=class_code)
            classroom.save()
            teacher = Teachers(teacher_id=request.user,classroom_id=classroom)
            teacher.save()
            return redirect('home')
        else:
            return render(request,'base/create_class.html',{'form':form}) 
    form = CreateClassForm()
    return render(request,'base/create_class.html',{'form':form})

def join_class(request):
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                classroom = Classrooms.objects.get(class_code=code)
            except Exception as e:
                return redirect('home')
            student = Students(student_id = request.user, classroom_id = classroom)
            student.save()
            return redirect('home')
        else:
            return render(request,'base/join_class.html',{'form':form})
    form = JoinClassForm()
    return render(request,'base/join_class.html',{'form':form})