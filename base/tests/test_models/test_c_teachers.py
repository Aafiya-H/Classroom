from django.test import TestCase
from django.conf import settings
from ...models import Teachers,CustomUser,Classrooms 

class TestTeachers(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestTeachers ,cls).setUpClass()
        Classrooms.objects.create(classroom_name='test_classroom',section='test_section',class_code='12345')
        CustomUser.objects.create(username='testuser',password='testpassword',email='testemail1234@gmail.com')
    
    def test_teacher_id(self):
        user = CustomUser.objects.get(pk=1)
        classroom = Classrooms.objects.get(pk=1)
        teacher = Teachers(teacher_id=user,classroom_id = classroom)
        field_value = teacher._meta.get_field('teacher_id').verbose_name
        self.assertEqual(field_value,'teacher id')
    
    def test_classroom_id(self):
        user = CustomUser.objects.get(pk=1)
        classroom = Classrooms.objects.get(pk=1)
        teacher = Teachers(teacher_id=user,classroom_id = classroom)
        field_value = teacher._meta.get_field('classroom_id').verbose_name
        self.assertEqual(field_value,'classroom id')

    def test_teacher_relation(self):
        user = CustomUser.objects.get(pk=1)
        classroom = Classrooms.objects.get(pk=1)
        Teachers.objects.create(teacher_id=user,classroom_id = classroom)
        self.assertEqual(Teachers.objects.filter(classroom_id=classroom).count(),1)