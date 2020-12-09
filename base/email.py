from django.core.mail import send_mail
from Classroom_project.settings import EMAIL_HOST_USER
from .models import Submissions,Assignments,Classrooms,Students,CustomUser
from datetime import datetime 

def send_email(subject,recipient,message):
    if isinstance(recipient,str):
        send_mail(subject,message,EMAIL_HOST_USER,recipient_list = [recipient],fail_silently = False)
    elif isinstance(recipient,list):
        send_mail(subject,message,EMAIL_HOST_USER,recipient_list = recipient,fail_silently = False)

def submission_marks_mail(submission_id,teacher_id,marks):
    teacher_name = CustomUser.objects.get(pk=teacher_id).username
    submission = Submissions.objects.get(pk=submission_id)
    assignment_name = submission.assignment_id.assignment_name
    student_user = submission.student_id.student_id
    student_username = student_user.username
    student_email = student_user.email
    message = 'Dear, {}, your submission for the assignment {} has been graded {} by Prof. {}'.format(student_username,assignment_name,marks,teacher_name)
    subject = 'Grading for assignment {}'.format(assignment_name)
    send_email(subject,student_email,message)

def assignment_post_mail(classroom_id,assignment_id):
    users = Students.objects.filter(classroom_id = classroom_id)
    email_list = [user.student_id.email for user in users]
    assignment = Assignments.objects.get(pk=assignment_id)
    assignment_name = assignment.assignment_name
    classroom_name = Classrooms.objects.get(pk=classroom_id.id).classroom_name
    due_date = assignment.due_date
    message = 'Dear Students, {} assignment has been posted to {}. Due date of the assignment is {}'.format(assignment_name,classroom_name,due_date)
    instructions = 'Instructions of the assignment are: {}'.format(assignment.instructions)
    message = message + '\n' + instructions
    subject = 'New Assignment in {} class'.format(classroom_name)
    send_email(subject,email_list,message)

def submission_done_mail(assignment_id,user,submitted_file):
    user_email = user.email 
    assignment = Assignments.objects.get(pk=assignment_id)
    assignment_name = assignment.assignment_name 
    message = 'Dear Student {}, you have made a submission {} for the assignment {} on {} .'.format(user.username,submitted_file.name,assignment_name,datetime.now())
    subject = 'File submitted for assignment {}'.format(assignment_name)
    send_email(subject,user_email,message)