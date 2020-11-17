from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from .utils import generate_class_code
from .decorators import access_class,login_excluded,teacher_required
from .models import * 
from .forms import *     

from itertools import chain

@login_excluded('home')
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

@login_required
def home(request):
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping) 
    return render(request,'base/home.html',{'mappings':mappings}) 

@access_class('home')
@login_required
def render_class(request,id):
    classroom = Classrooms.objects.get(pk=id)
    try: 
        assignments = Assignments.objects.filter(classroom_id = id)
    except Exception as e:
        assignments = None

    try:
        students = Students.objects.filter( classroom_id = id)
    except Exception as e:
        students = None
    
    teachers = Teachers.objects.filter(classroom_id = id)
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping) 
    return render(request,'base/class_page.html',{'classroom':classroom,'assignments':assignments,'students':students,'teachers':teachers,"mappings":mappings})

@login_required
def assignment_summary(request,assignment_id):
    assignment = Assignments.objects.filter(pk = assignment_id).first()
    submissions = Submissions.objects.filter(assignment_id = assignment_id)
    teachers = Teachers.objects.filter(classroom_id = assignment.classroom_id)

    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping)
    # print(submissions)
    return render(request,'base/assignment_summary.html',{'assignment':assignment,'submissions':submissions,'mappings':mappings})

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

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
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

@login_required
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

@teacher_required('home')
@login_required
def create_assignment(request,classroom_id):
    if request.method == 'POST':
        form = CreateAssignmentForm(request.POST)
        if form.is_valid():
            assignment_name = form.cleaned_data.get('assignment_name')
            due_date = form.cleaned_data.get('due_date')
            classroom_id = Classrooms.objects.get(pk=classroom_id)
            instructions = form.cleaned_data.get('instructions')
            total_marks = form.cleaned_data.get('total_marks')
            assignment = Assignments(assignment_name = assignment_name,due_date = due_date,instructions = instructions,total_marks = total_marks,classroom_id=classroom_id)
            assignment.save()
            return redirect('render_class',id=classroom_id.id)
        else:
            return render(request,'base/create_assignment.html',{'form':form})
    form = CreateAssignmentForm()
    return render(request,'base/create_assignment.html',{'form':form}) 
