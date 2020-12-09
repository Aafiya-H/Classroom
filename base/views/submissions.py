from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..decorators import student_required
from ..models import Assignments, Students, Submissions
from ..forms import *     
from .. import email

from datetime import datetime

@csrf_exempt
@login_required(login_url='login')
@student_required('home')
def submit_assignment_request(request,assignment_id):
    assignment = Assignments.objects.get(pk=assignment_id)
    student_id = Students.objects.get(classroom_id=assignment.classroom_id,student_id=request.user.id)
    file_name = request.FILES.get('myfile')
    try:
        submission = Submissions.objects.get(assignment_id=assignment, student_id = student_id)
        submission.submission_file = file_name
        submission.save()
        return JsonResponse({'status':'SUCCESS'})

    except Exception as e:  
        print(str(e))  
        submission = Submissions(assignment_id = assignment,student_id= student_id,submission_file = file_name)
        dt1=datetime.now()
        dt2=datetime.combine(assignment.due_date,assignment.due_time)
        time = timesince(dt1, dt2)
        if time[0]=='0':
            submission.submitted_on_time=False
        submission.save()
        email.submission_done_mail(assignment_id,request.user,file_name)
        return JsonResponse({'status':'SUCCESS'})

def mark_submission_request(request,submission_id,teacher_id):
    if request.POST.get('action') == 'post':
        marks = request.POST.get('submission_marks')
        submission = Submissions.objects.get(pk=submission_id)
        submission.marks_alloted = marks
        submission.save()
        email.submission_marks_mail(submission_id,teacher_id,marks)
        return JsonResponse({'status':'SUCCESS'})