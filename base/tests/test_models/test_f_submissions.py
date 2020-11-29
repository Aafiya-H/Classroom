from django.test import TestCase 
from django.core.files import File

from datetime import timedelta
import datetime 
from freezegun import freeze_time
import mock 

from ...models import CustomUser,Assignments,Submissions,Students,Classrooms

class TestSubmissions(TestCase):
    @classmethod
    @freeze_time('2020-10-04')
    def setUpClass(cls):
        super(TestSubmissions ,cls).setUpClass()
        Classrooms.objects.create(classroom_name='test_classroom',section='test_section',class_code='12345')
        classroom = Classrooms.objects.get(pk=1)
        Assignments.objects.create(assignment_name='test_assignment',classroom_id=classroom,due_date=datetime.datetime.now() + timedelta(days=3),instructions='This is a test assignment',total_marks=20)
        CustomUser.objects.create(username='testuser',password='testpassword',email='testemail1234@gmail.com')
        mock_file = mock.MagicMock(spec=File)
        mock_file.name = 'test.pdf'
        assignment = Assignments.objects.get(pk=1)
        user = CustomUser.objects.get(pk=1)
        Students.objects.create(student_id=user,classroom_id=classroom)
        student_id = Students.objects.get(pk=1)
        Submissions.objects.create(assignment_id=assignment,student_id=student_id,submitted_on_time=True,marks_alloted=10,submission_file=mock_file)
    
    def test_assignment_id(self):
        submission = Submissions.objects.get(pk=1)
        field_label = submission._meta.get_field('assignment_id').verbose_name
        self.assertEqual(field_label,'assignment id')
    
    def test_assignment_relation(self):
        assignment = Assignments.objects.get(pk=1)
        self.assertEqual(Submissions.objects.filter(assignment_id=assignment).count(),1)
    
    def test_student_id(self):
        submission = Submissions.objects.get(pk=1)
        field_label = submission._meta.get_field('student_id').verbose_name
        self.assertEqual(field_label,'student id')
    
    def test_student_relation(self):
        student_mapping = Students.objects.get(pk=1)
        self.assertEqual(Submissions.objects.filter(student_id=student_mapping).count(),1)

    def test_submitted_date(self):
        submission = Submissions.objects.get(pk=1)
        field_value = submission._meta.get_field('submitted_date').verbose_name 
        self.assertEqual(field_value,'submitted date')

    def test_submitted_date_value(self):
        submission = Submissions.objects.get(pk=1)
        self.assertEqual(submission.submitted_date,datetime.date(2020,10,4))
    
    def test_submitted_on_time(self):
        submission = Submissions.objects.get(pk=1)
        field_value = submission._meta.get_field('submitted_on_time').verbose_name 
        self.assertEqual(field_value,'submitted on time')
    
    def test_submitted_on_time_default(self):   
        submission = Submissions.objects.get(pk=1)
        default = submission._meta.get_field('submitted_on_time').default 
        self.assertEqual(default,True)
    
    def test_marks_alloted(self):
        submission = Submissions.objects.get(pk=1)
        field_value = submission._meta.get_field('marks_alloted').verbose_name 
        self.assertEqual(field_value,'marks alloted')
    
    def test_marks_alloted_default(self):
        submission = Submissions.objects.get(pk=1)
        default = submission._meta.get_field('marks_alloted').default 
        self.assertEqual(default,0)
    
    def test_submission_file(self):
        submission = Submissions.objects.get(pk=1)
        field_value = submission._meta.get_field('submission_file').verbose_name 
        self.assertEqual(field_value,'submission file')