from django.test import TestCase
from django.urls import reverse
from datetime import timedelta
import datetime 
from ...views import Assignments, Teachers 

class Testcreate_assignment():
    @classmethod
    def teacher_id_check(self):
        user = CustomUser.objects.get(pk=1)
        assignment = Assigmets.objects.get(pk=1)
        teacher = Teachers(teacher_id=user,classroom_id = assignment.classroom_id)
        field_value = teacher._meta.get_field('teacher_id').verbose_name
        self.assertEqual(field_value,'teacher id')

class Test_assignment_summary():
    @classmethod
    def teacher_id_check(self):
        user = CustomUser.objects.get(pk=1)
        assignment = Assigmets.objects.get(pk=1)
        teacher = Teachers(teacher_id=user,classroom_id = assignment.classroom_id)
        field_value = teacher._meta.get_field('teacher_id').verbose_name
        self.assertEqual(field_value,'teacher id')


