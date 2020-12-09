from django.test import TestCase 
from django.urls import reverse,resolve

class TestClassUrls(TestCase):
    def test_class_reverse(self): 
        url = reverse('render_class',args=[1])
        self.assertEqual(url,'/class/1')

    def test_class_resolve(self):
        resolver = resolve('/class/1')
        self.assertEqual(resolver.view_name,'render_class')
    
    def test_unenroll_class_reverse(self):
        url = reverse('unenroll_class',args=[1])
        self.assertEqual(url,'/unenroll_class/1')
    
    def test_unenroll_class_resolve(self):
        resolver = resolve('/unenroll_class/1')
        self.assertEqual(resolver.view_name,'unenroll_class')
    
    def test_delete_class_reverse(self):
        url = reverse('delete_class',args=[1])
        self.assertEqual(url,'/delete_class/1')

    def test_delete_class_resolve(self):
        resolver = resolve('/delete_class/1')
        self.assertEqual(resolver.view_name,'delete_class')
    
    def test_create_class_reverse(self):
        url = reverse('create_class_request')
        self.assertEqual(url,'/create_class_request/')
    
    def test_create_class_resolve(self):
        resolver = resolve('/create_class_request/')
        self.assertEqual(resolver.view_name,'create_class_request')

    def test_join_class_reverse(self):
        url = reverse('join_class_request')
        self.assertEqual(url,'/join_class_request/')
    
    def test_join_class_resolve(self):
        resolver = resolve('/join_class_request/')
        self.assertEqual(resolver.view_name,'join_class_request')