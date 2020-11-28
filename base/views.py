from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import generate_class_code
from .decorators import access_class,login_excluded,teacher_required,student_required
from .models import * 
from .forms import *     
from . import email

from itertools import chain

def landing_page(request):
    return render(request,'base/landing_index.html')

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

@login_required
def home(request):
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping) 
    return render(request,'base/home.html',{'mappings':mappings}) 

@login_required
@teacher_required('home')
def delete_assignment(request,assignment_id):
    assignment = Assignments.objects.filter(pk=assignment_id)
    if assignment.count() == 0:
        return redirect('home')
    else:
        classroom_id = assignment.classroom_id.id 
        Assignments.objects.filter(pk=assignment_id).delete()
        return redirect('render_class', id=classroom_id)

@login_required
@student_required('home')
def unenroll_class(request,classroom_id):
    classroom = Classrooms.objects.get(pk=classroom_id)
    student_mapping = Students.objects.filter(student_id=request.user,classroom_id=classroom).delete()
    return redirect('home')

@login_required
@teacher_required('home')
def delete_class(request,classroom_id):
    classroom = Classrooms.objects.get(pk=classroom_id)
    teacher_mapping = Teachers.objects.get(teacher_id=request.user,classroom_id=classroom)
    teacher_mapping.delete()
    classroom.delete()
    return redirect('home')

@login_required
@access_class('home')
def render_class(request,id):
    classroom = Classrooms.objects.get(pk=id)
    try: 
        assignments = Assignments.objects.filter(classroom_id = id)
    except Exception as e:
        assignments = None

    try:
        students = Students.objects.filter(classroom_id = id)
    except Exception as e:
        students = None
    
    teachers = Teachers.objects.filter(classroom_id = id)
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping) 
    return render(request,'base/class_page.html',{'classroom':classroom,'assignments':assignments,'students':students,'teachers':teachers,"mappings":mappings})

@login_required
@teacher_required('home')
def assignment_summary(request,assignment_id):
    assignment = Assignments.objects.filter(pk = assignment_id).first()
    submissions = Submissions.objects.filter(assignment_id = assignment_id)
    teachers = Teachers.objects.filter(classroom_id = assignment.classroom_id)
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping)
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
@teacher_required('home')
def create_assignment(request,classroom_id):
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping)

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
            email.assignment_post_mail(classroom_id,assignment.id)
            return redirect('render_class',id=classroom_id.id)
        else:
            return render(request,'base/create_assignment.html',{'form':form,'mappings':mappings})
    form = CreateAssignmentForm()
    return render(request,'base/create_assignment.html',{'form':form,'mappings':mappings})

@login_required
def create_class_request(request):
    if request.POST.get('action') == 'post':
        classrooms = Classrooms.objects.all()
        existing_codes=[]
        for classroom in classrooms:
            existing_codes.append(classroom.class_code)
        
        class_name = request.POST.get('class_name')
        section = request.POST.get('section')

        class_code = generate_class_code(6,existing_codes)
        classroom = Classrooms(classroom_name=class_name,section=section,class_code=class_code)
        classroom.save()
        teacher = Teachers(teacher_id=request.user,classroom_id=classroom)
        teacher.save()
        return JsonResponse({'status':'SUCCESS'})

@login_required
def join_class_request(request):
    if request.POST.get('action') == 'post':
        code = request.POST.get('class_code')
        try:
            classroom = Classrooms.objects.get(class_code=code)
        except Exception as e:
            print(e)
            return JsonResponse({'status':'FAIL','message':str(e)})
        student = Students(student_id = request.user, classroom_id = classroom)
        student.save()
        return JsonResponse({'status':'SUCCESS'})

@csrf_exempt
@login_required
@student_required('home')
def submit_assignment_request(request,assignment_id):
    assignment = Assignments.objects.get(pk=assignment_id)
    student_id = Students.objects.get(classroom_id=assignment.classroom_id,student_id=request.user.id)
    file_name = request.FILES.get('myfile')
    try:
        submission = Submissions.objects.get(assignment_id=assignment, student_id = student_id)
        print('-'*20)
        print('hello from submit_assignment_request')
        print('-'*20)
        submission.submission_file = file_name
        submission.save()
        return JsonResponse({'status':'SUCCESS'})

    except Exception as e:  
        print(str(e))  
        submission = Submissions(assignment_id = assignment,student_id= student_id,submission_file = file_name)
        submission.save()
        email.submission_done_mail(assignment_id,request.user,file_name)
        return JsonResponse({'status':'SUCCESS'})

def temp_mail_view(request): 
    email.send_email('Heyy','talha.c@somaiya.edu','Test Email using django')
    return redirect('home')

def mark_submission_request(request,submission_id,teacher_id):
    if request.POST.get('action') == 'post':
        marks = request.POST.get('submission_marks')
        print('-'*20)
        print('From mark_submission_request')
        print(marks)
        print(submission_id)
        print('-'*20)
        submission = Submissions.objects.get(pk=submission_id)
        submission.marks_alloted = marks
        submission.save()
        email.submission_marks_mail(submission_id,teacher_id,marks)
        return JsonResponse({'status':'SUCCESS'})
        