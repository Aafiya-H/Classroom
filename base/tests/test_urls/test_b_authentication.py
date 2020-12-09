from django.test import TestCase 
from django.urls import reverse,resolve

class TestAuthUrls(TestCase):
    def test_login_reverse(self): 
        url = reverse('login')
        self.assertEqual(url,'/login/')

    def test_login_resolve(self):
        resolver = resolve('/login/')
        self.assertEqual(resolver.view_name,'login')

    def test_register_reverse(self):
        url = reverse('register')
        self.assertEqual(url,'/register/')

    def test_register_resolve(self):
        resolver = resolve('/register/')
        self.assertEqual(resolver.view_name,'register') 

    def test_logout_reverse(self):
        url = reverse('logout')
        self.assertEqual(url,'/logout/')
    
    def test_logout_resolve(self):
        resolver = resolve('/logout/')
        self.assertEqual(resolver.view_name,'logout')