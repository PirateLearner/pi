"""
Test cases for the PirateLearner Project Entry Points
"""

from django.test import TestCase
from selenium import webdriver

from django.core.urlresolvers import resolve
from blogging import views

class HomePageTest(TestCase):
    def test_homepage_url_resolve(self):
        self.assertEqual(1+1, 2, "1+1 !=2")
        