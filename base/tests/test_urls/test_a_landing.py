from django.test import TestCase 
from django.urls import reverse,resolve

class TestLandingUrls(TestCase):
    def test_landing_reverse(self): 
        url = reverse('landing_page')
        self.assertEqual(url,'/')

    def test_landing_resolve(self):
        resolver = resolve('/')
        self.assertEqual(resolver.view_name,'landing_page')

    def test_home_reverse(self):
        url = reverse('home')
        self.assertEqual(url,'/home/')

    def test_home_resolve(self):
        resolver = resolve('/home/')
        self.assertEqual(resolver.view_name,'home') 