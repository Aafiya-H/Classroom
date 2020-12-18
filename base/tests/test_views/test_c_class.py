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
        test_student = CustomUser.objects.create(username='test_student',password='test_password',email='test_student1234@gmail.com')
        test_student.set_password('test_password')
        test_student.save()

        test_teacher = CustomUser.objects.create(username='test_teacher',password='test_password',email='test_teacher1234@gmail.com') 
        test_teacher.set_password('test_password')
        test_teacher.save()
        

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
        print(login)
        print(reverse('render_class',kwargs = {'id':1}))
        response = self.client.get(reverse('render_class',kwargs = {'id':1}))
        self.assertEqual(response.status_code,200)
        context = response.context
        self.assertTrue(isinstance(context['classroom'],Classrooms))
        self.assertTemplateUsed(response,'base/class_page.html')
    
    def test_d_unenroll_class_view(self):
        pass
    
    def test_e_delete_class_view(self):
        pass