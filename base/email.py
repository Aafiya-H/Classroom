from django.core.mail import send_mail
from Classroom_project.settings import EMAIL_HOST_USER

def send_email(recipient,message):
    send_mail('Welcome',message,EMAIL_HOST_USER,[recipient],fail_silently = False)