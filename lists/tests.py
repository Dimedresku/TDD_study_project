from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

class HomePageTest(TestCase):
    '''home page test'''

    def test_uses_home_template(self):
        '''test: home page return correct html'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')