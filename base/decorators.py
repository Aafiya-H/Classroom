from django.contrib.auth.models import User 
from django.shortcuts import redirect

from .models import Classrooms,Students,Teachers

def access_class(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request,*args, **kwargs):
            not_a_teacher,not_a_student = False,False
            try:
                classroom = Classrooms.objects.get(id=kwargs['id'])
            except Exception as e:
                return redirect('home')

            teacher_count = Teachers.objects.filter(teacher_id=request.user.id, classroom_id=classroom).count()
            if teacher_count > 0:
                not_a_teacher = True

            student_count = Students.objects.filter(student_id=request.user.id, classroom_id=classroom).count()
            if student_count > 0:
                not_a_student = True 

            if not (not_a_student or not_a_teacher):
                return redirect('home')

            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

def login_excluded(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to) 
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

def teacher_required(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            try:
                classroom = Classrooms.objects.get(pk=kwargs['classroom_id'])
            except Exception as e:
                return redirect('render_class',id=kwargs['classroom_id'])

            teacher_count = Teachers.objects.filter(teacher_id=request.user,classroom_id=classroom).count()
            if teacher_count == 0:
                return redirect('render_class',id=kwargs['classroom_id'])
            return view_method(request,*args,**kwargs)
        return _arguments_wrapper
    return _method_wrapper 