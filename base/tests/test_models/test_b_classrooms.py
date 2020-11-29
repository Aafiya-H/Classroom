from django.test import TestCase 
from ...models import Classrooms

class TestClassrooms(TestCase):
    @classmethod 
    def setUpClass(cls):
        super(TestClassrooms ,cls).setUpClass()
        Classrooms.objects.create(classroom_name='test_classroom',section='test_section',class_code='12345')

    def test_classroom_name(self):
        classroom = Classrooms.objects.get(id=1)
        field_label = classroom._meta.get_field('classroom_name').verbose_name
        self.assertEqual(field_label,'classroom name')

    def test_classroom_name_max_length(self):
        classroom = Classrooms.objects.get(id=1)
        max_length = classroom._meta.get_field('classroom_name').max_length
        self.assertEqual(max_length,100)

    def test_section(self):
        classroom = Classrooms.objects.get(id=1)
        field_label = classroom._meta.get_field('section').verbose_name
        self.assertEqual(field_label,'section') 

    def test_section_max_length(self):
        classroom = Classrooms.objects.get(id=1)
        max_length = classroom._meta.get_field('section').max_length
        self.assertEqual(max_length,100)

    def test_section_default(self):
        classroom = Classrooms.objects.get(id=1)
        default = classroom._meta.get_field('section').default
        self.assertEqual(default,'Third Year') 

    def test_class_code(self):
        classroom = Classrooms.objects.get(id=1)
        field_label = classroom._meta.get_field('class_code').verbose_name
        self.assertEqual(field_label,'class code')
    
    def test_class_code_max_length(self):
        classroom = Classrooms.objects.get(id=1)
        max_length = classroom._meta.get_field('class_code').max_length
        self.assertEqual(max_length,10)
    
    def test_class_code_default(self):
        classroom = Classrooms.objects.get(id=1)
        default = classroom._meta.get_field('class_code').default
        self.assertEqual(default,'0000000')