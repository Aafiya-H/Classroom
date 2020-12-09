from django.test import TestCase 
from django.urls import reverse,resolve

class TestSubmissionUrls(TestCase):
    def test_mark_submission_request_reverse(self):
        url = reverse('mark_submission_request',args=[1,1])
        self.assertEqual(url,'/mark_submission_request/1/1')

    def test_mark_submission_request_resolve(self):
        resolver = resolve('/mark_submission_request/1/1')
        self.assertEqual(resolver.view_name,'mark_submission_request')