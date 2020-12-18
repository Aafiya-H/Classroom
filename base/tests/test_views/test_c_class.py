from django.test import TestCase
from django.contrib.auth.decorators import login_required
from django.urls import reverse 
from django.db.models.query import QuerySet
from django.conf import settings
import json
from itertools import chain

from ...models import CustomUser, Classrooms, Students, Teachers

class TestClassroomViews(TestCase):
    def setUp(self):
        self.test_student = CustomUser.objects.create(username='test_student',password='test_password',email='test_student1234@gmail.com')
        self.test_student.set_password('test_password')
        self.test_student.save()

        self.test_teacher = CustomUser.objects.create(username='test_teacher',password='test_password',email='test_teacher1234@gmail.com') 
        self.test_teacher.set_password('test_password')
        self.test_teacher.save()
        

    def test_a_create_class_view(self):
        login = self.client.login(username='test_teacher',password='test_password')
        response = self.client.post(reverse('create_class_request'),{'class_name':'Test_class_2','section':'TY A','action':'post'})
        self.assertEqual(json.loads(response.content)['status'],'SUCCESS')
    
    def test_b_join_class_view(self):
        login = self.client.login(username='test_student',password='test_password')
        test_classroom = Classrooms.objects.create(classroom_name='Test_Class',section='Test_Section',class_code='123456')
        response = self.client.post(reverse('join_class_request'),{'class_code':'123456','action':'post'})
        self.assertEqual(json.loads(response.content)['status'],'SUCCESS')

    def test_c_render_class_view(self):
        login = self.client.login(username='test_student',password='test_password')
        test_classroom = Classrooms.objects.create(classroom_name='Test_Class',section='Test_Section',class_code='123456')
        student_entry = Students.objects.create(student_id = self.test_student,classroom_id = test_classroom)
        response = self.client.get(reverse('render_class',kwargs = {'id':1}))
        self.assertEqual(response.status_code,200)
        context = response.context
        self.assertTrue(isinstance(context['classroom'],Classrooms))
        self.assertTemplateUsed(response,'base/class_page.html')
    
    def test_d_unenroll_class_view(self):
        login = self.client.login(username='test_student',password = 'test_password')
        test_classroom = Classrooms.objects.create(classroom_name='Test_Class',section='Test_Section',class_code='123456')
        student_entry = Students.objects.create(student_id = self.test_student,classroom_id = test_classroom)
        response = self.client.get(reverse('unenroll_class',kwargs={'classroom_id':1}))
        self.assertEqual(response.status_code,302)
        student_class_mapping = Students.objects.filter(student_id = self.test_student, classroom_id = test_classroom)
        self.assertEqual(student_class_mapping.count(), 0)
    
    def test_e_delete_class_view(self):
        login = self.client.login(username='test_teacher',password = 'test_password')
        test_classroom = Classrooms.objects.create(classroom_name='Test_Class',section='Test_Section',class_code='123456')
        teacher_entry = Teachers.objects.create(teacher_id = self.test_teacher,classroom_id = test_classroom)
        response = self.client.get(reverse('delete_class',kwargs={'classroom_id':1}))
        self.assertEqual(response.status_code,302)

        teacher_class_mapping = Teachers.objects.filter(teacher_id = self.test_teacher, classroom_id = test_classroom)
        self.assertEqual(teacher_class_mapping.count(), 0)

        test_classroom = Classrooms.objects.filter(id = 1)
        self.assertEqual(test_classroom.count(),0)
