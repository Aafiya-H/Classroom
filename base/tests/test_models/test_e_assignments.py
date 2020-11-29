from django.test import TestCase
from datetime import timedelta
import datetime 
from freezegun import freeze_time

from ...models import Assignments,Classrooms

class TestAssignments(TestCase):
    @classmethod
    @freeze_time('2020-10-03')
    def setUpClass(cls):
        super(TestAssignments ,cls).setUpClass()
        Classrooms.objects.create(classroom_name='test_classroom',section='test_section',class_code='12345')
        classroom = Classrooms.objects.get(pk=1)
        Assignments.objects.create(assignment_name='test_assignment',classroom_id=classroom,due_date=datetime.datetime.now() + timedelta(days=3),instructions='This is a test assignment',total_marks=20)
    
    def test_assignment_name(self):
        assignment = Assignments.objects.get(pk=1)
        field_label = assignment._meta.get_field('assignment_name').verbose_name
        self.assertEqual(field_label,'assignment name')
    
    def test_assignment_max_length(self):
        assignment = Assignments.objects.get(pk=1)
        max_length = assignment._meta.get_field('assignment_name').max_length
        self.assertEqual(max_length,50)
    
    def test_classroom_id(self):
        assignment = Assignments.objects.get(pk=1)
        field_label = assignment._meta.get_field('classroom_id').verbose_name
        self.assertEqual(field_label,'classroom id')
    
    def test_classroom_relation(self):
        classroom = Classrooms.objects.get(pk=1)
        self.assertEqual(Assignments.objects.filter(classroom_id=classroom).count(),1)

    def test_due_date(self):
        assignment = Assignments.objects.get(pk=1)
        field_label = assignment._meta.get_field('due_date').verbose_name
        self.assertEqual(field_label,'due date')
    
    def test_due_date_value(self):
        assignment  = Assignments.objects.get(pk=1)
        self.assertEqual(assignment.due_date,datetime.date(2020,10,3) + timedelta(days=3))

    def test_posted_date(self):
        assignment = Assignments.objects.get(pk=1)
        field_label = assignment._meta.get_field('posted_date').verbose_name
        self.assertEqual(field_label,'posted date')

    def test_posted_date_value(self):
        assignment  = Assignments.objects.get(pk=1)
        self.assertEqual(assignment.posted_date,datetime.date(2020,10,3)) 

    def test_instructions(self):
        assignment = Assignments.objects.get(pk=1)
        field_label = assignment._meta.get_field('instructions').verbose_name
        self.assertEqual(field_label,'instructions')

    def test_total_marks(self):
        assignment = Assignments.objects.get(pk=1)
        field_label = assignment._meta.get_field('total_marks').verbose_name
        self.assertEqual(field_label,'total marks')

    def test_total_marks_default(self):
        assignment = Assignments.objects.get(pk=1)
        defualt_value = assignment._meta.get_field('total_marks').default
        self.assertEqual(defualt_value,100)