from django.test import TestCase
from django.contrib.auth.decorators import login_required
from django.urls import reverse 
from django.db.models.query import QuerySet
from django.conf import settings

from itertools import chain

from ...models import CustomUser, Classrooms, Students, Teachers

class TestHomeViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestHomeViews ,cls).setUpClass()

        test_student = CustomUser.objects.create(username='test_student',password='test_password',email='test_student1234@gmail.com')
        test_student.set_password('test_password')
        test_student.save()

        test_teacher = CustomUser.objects.create(username='test_teacher',password='test_password',email='test_teacher1234@gmail.com') 
        test_teacher.set_password('test_password')
        test_teacher.save()

        test_classroom = Classrooms.objects.create(classroom_name='test_classroom',section='test_section',class_code='12345')
        
        Students.objects.create(student_id=test_student,classroom_id = test_classroom)
        Teachers.objects.create(teacher_id=test_teacher,classroom_id = test_classroom)

    def test_a_landing_response(self):
        response = self.client.get(reverse('landing_page')) 
        self.assertEqual(response.status_code,200)

    def test_b_landing_template(self):
        response = self.client.get(reverse('landing_page')) 
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'base/landing.html')
    
    def test_c_home_view(self):
        login = self.client.login(username='test_student',password='test_password')
        response = self.client.get('/home/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'base/home.html')

    def test_d_home_context(self):
        login = self.client.login(username='test_student',password='test_password')
        response = self.client.get('/home/')
        self.assertEqual(response.status_code,200)
        context = response.context
        self.assertTrue(isinstance(context['teachers_all'],QuerySet))
        self.assertTrue(isinstance(context['mappings'],chain))

    def test_e_check_home_output_length(self):
        login = self.client.login(username='test_teacher',password='test_password')
        response = self.client.get('/home/')
        self.assertEqual(response.status_code,200)
        context = response.context
        self.assertEqual(len(context['teachers_all']),1)
        