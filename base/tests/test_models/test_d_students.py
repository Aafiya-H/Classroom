from django.test import TestCase
from ...models import Teachers,CustomUser,Classrooms,Students 

class TestStudents(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestStudents ,cls).setUpClass()
        Classrooms.objects.create(classroom_name='test_classroom',section='test_section',class_code='12345')
        CustomUser.objects.create(username='testuser',password='testpassword',email='testemail1234@gmail.com')
    
    def test_student_id(self):
        user = CustomUser.objects.get(pk=1)
        classroom = Classrooms.objects.get(pk=1)
        student = Students(student_id=user,classroom_id = classroom)
        field_value = student._meta.get_field('student_id').verbose_name
        self.assertEqual(field_value,'student id')
    
    def test_classroom_id(self):
        user = CustomUser.objects.get(pk=1)
        classroom = Classrooms.objects.get(pk=1)
        student = Students(student_id=user,classroom_id = classroom)
        field_value = student._meta.get_field('classroom_id').verbose_name
        self.assertEqual(field_value,'classroom id')    

    def test_student_relation(self):
        user = CustomUser.objects.get(pk=1)
        classroom = Classrooms.objects.get(pk=1)
        Students.objects.create(student_id=user,classroom_id = classroom)
        self.assertEqual(Students.objects.filter(classroom_id=classroom).count(),1)