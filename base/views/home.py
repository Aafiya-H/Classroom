from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Students,Teachers

from itertools import chain

def landing_page(request):
    return render(request,'base/landing.html')

@login_required(login_url='login')
def home(request):
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    teachers_all = Teachers.objects.all()
    mappings = chain(teacher_mapping,student_mapping) 
    return render(request,'base/home.html',{'mappings':mappings,'teachers_all':teachers_all}) 