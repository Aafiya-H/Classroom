from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Classrooms(models.Model):
    classroom_name=models.CharField(max_length=100)

class Students(models.Model):
    student_id=models.ForeignKey(User,on_delete=models.CASCADE)
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE)

class Teachers(models.Model):
    teacher_id=models.ForeignKey(User,on_delete=models.CASCADE)
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE) 

class Assignments(models.Model):
    assignment_name=models.CharField(max_length=50)
    classroom_id=models.ForeignKey(Classrooms,on_delete=models.CASCADE)
    due_date=models.DateField()
    posted_date=models.DateField(auto_now_add=True)
    instructions=models.TextField()
    total_marks=models.IntegerField(default=100)

class Submissions(models.Model):
    assignment_id=models.ForeignKey(Assignments,on_delete=models.CASCADE)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    submitted_date=models.DateField(auto_now_add=True)
    submitted_on_time=models.BooleanField()
    marks_alloted=models.IntegerField(default=0)

