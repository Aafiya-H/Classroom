from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from ..utils import generate_class_code
from ..decorators import access_class,teacher_required,student_required
from ..models import Classrooms, Teachers, Students, Assignments

from itertools import chain

@login_required(login_url='login')
@student_required('home')
def unenroll_class(request,classroom_id):
    classroom = Classrooms.objects.get(pk=classroom_id)
    student_mapping = Students.objects.filter(student_id=request.user,classroom_id=classroom).delete()
    return redirect('home')

@login_required(login_url='login')
@teacher_required('home')
def delete_class(request,classroom_id):
    classroom = Classrooms.objects.get(pk=classroom_id)
    teacher_mapping = Teachers.objects.get(teacher_id=request.user,classroom_id=classroom)
    teacher_mapping.delete()
    classroom.delete()
    return redirect('home')

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def join_class_request(request):
    if request.POST.get('action') == 'post':
        code = request.POST.get('class_code')
        try:
            classroom = Classrooms.objects.get(class_code=code)
            student = Students.objects.filter(student_id = request.user, classroom_id = classroom)
            if (student.count()!=0):
                return redirect('home')
        except Exception as e:
            print(e)
            return JsonResponse({'status':'FAIL','message':str(e)})
        student = Students(student_id = request.user, classroom_id = classroom)
        student.save()
        return JsonResponse({'status':'SUCCESS'})