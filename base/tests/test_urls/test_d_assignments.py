from django.test import TestCase 
from django.urls import reverse,resolve

class TestAssignmentUrls(TestCase):
    def test_create_assignment_reverse(self): 
        url = reverse('create_assignment',args=[1])
        self.assertEqual(url,'/create_assignment/1')

    def test_create_assignment_resolve(self):
        resolver = resolve('/create_assignment/1')
        self.assertEqual(resolver.view_name,'create_assignment')

    def test_assignment_summary_reverse(self):
        url = reverse('assignment_summary',args=[1])
        self.assertEqual(url,'/assignment_summary/1')

    def test_assignment_summary_resolve(self):
        resolver = resolve('/assignment_summary/1')
        self.assertEqual(resolver.view_name,'assignment_summary')

    def test_delete_assignment_reverse(self):
        url = reverse('delete_assignment',args=[1])
        self.assertEqual(url,'/delete_assignment/1')

    def test_delete_assignment_resolve(self):
        resolver = resolve('/delete_assignment/1')
        self.assertEqual(resolver.view_name,'delete_assignment')
    
    def test_submit_assignment_request_reverse(self):
        url = reverse('submit_assignment_request',args=[1])
        self.assertEqual(url,'/submit_assignment_request/1')

    def test_submit_assignment_request_resolve(self):
        resolver = resolve('/submit_assignment_request/1')
        self.assertEqual(resolver.view_name,'submit_assignment_request')
    