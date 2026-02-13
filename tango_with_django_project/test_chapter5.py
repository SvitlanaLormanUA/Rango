import os
import unittest
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
django.setup()

from rango.models import Category, Page
from django.contrib.auth.models import User
from django.contrib import admin
from rango.admin import PageAdmin

class Chapter5Tests(unittest.TestCase):
    def test_category_model_fields(self):
        """
        Check if the Category model has the required fields: views and likes.
        """
        category = Category()
        self.assertTrue(hasattr(category, 'views'), "Category model does not have a 'views' field.")
        self.assertTrue(hasattr(category, 'likes'), "Category model does not have a 'likes' field.")

    def test_category_model_defaults(self):
        """
        Check if the default values for views and likes are 0.
        """
        c = Category.objects.create(name="Test Category Defaults")
        self.assertEqual(c.views, 0, "Default value for views should be 0.")
        self.assertEqual(c.likes, 0, "Default value for likes should be 0.")
        c.delete()

    def test_population_script_execution(self):
        """
        Check if the population script created the correct data.
        """
        # Check Python category
        try:
            python_cat = Category.objects.get(name='Python')
            self.assertEqual(python_cat.views, 128, "Python category views should be 128.")
            self.assertEqual(python_cat.likes, 64, "Python category likes should be 64.")
        except Category.DoesNotExist:
            self.fail("Python category was not found. Did you run the population script?")

        # Check Django category
        try:
            django_cat = Category.objects.get(name='Django')
            self.assertEqual(django_cat.views, 64, "Django category views should be 64.")
            self.assertEqual(django_cat.likes, 32, "Django category likes should be 32.")
        except Category.DoesNotExist:
            self.fail("Django category was not found. Did you run the population script?")

        # Check Other Frameworks category
        try:
            other_cat = Category.objects.get(name='Other Frameworks')
            self.assertEqual(other_cat.views, 32, "Other Frameworks category views should be 32.")
            self.assertEqual(other_cat.likes, 16, "Other Frameworks category likes should be 16.")
        except Category.DoesNotExist:
            self.fail("Other Frameworks category was not found. Did you run the population script?")

    def test_admin_interface_page_display(self):
        """
        Check if the PageAdmin is configured correctly.
        """
        self.assertIn('category', PageAdmin.list_display, "PageAdmin list_display should include 'category'.")
        self.assertIn('title', PageAdmin.list_display, "PageAdmin list_display should include 'title'.")
        self.assertIn('url', PageAdmin.list_display, "PageAdmin list_display should include 'url'.")
        
        # Check order
        expected_order = ('category', 'title', 'url')
        self.assertEqual(PageAdmin.list_display, expected_order, f"PageAdmin list_display should be {expected_order}.")

if __name__ == '__main__':
    unittest.main()