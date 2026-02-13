import os
import unittest
import django
from django.test import Client
from django.urls import reverse

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
django.setup()

from rango.models import Category, Page

class Chapter6Tests(django.test.TestCase):
    def setUp(self):
        self.client = Client()

    def test_category_slug_field(self):
        """
        Check if the Category model has the 'slug' field.
        """
        category = Category()
        self.assertTrue(hasattr(category, 'slug'), "Category model does not have a 'slug' field.")

    def test_slug_creation(self):
        """
        Check if the slug is automatically created when saving a category.
        """
        c = Category.objects.create(name="Test Slug Creation")
        self.assertEqual(c.slug, "test-slug-creation", "Slug was not created correctly.")
        c.delete()

    def test_page_views_field(self):
        """
        Check if the population script added views to pages.
        """
        # We assume the population script has been run.
        # Check a known page
        try:
            p = Page.objects.get(title="Official Python Tutorial")
            self.assertEqual(p.views, 100, "Official Python Tutorial should have 100 views.")
        except Page.DoesNotExist:
            self.fail("Official Python Tutorial page not found. Did you run the updated population script?")

    def test_index_view_context(self):
        """
        Check if the index view context contains 'categories' and 'pages'.
        """
        response = self.client.get(reverse('rango:index'))
        self.assertTrue('categories' in response.context, "Index context should contain 'categories'.")
        self.assertTrue('pages' in response.context, "Index context should contain 'pages'.")
        self.assertEqual(len(response.context['pages']), 5, "Index should display top 5 pages.")

    def test_category_view(self):
        """
        Check if the category view works correctly.
        """
        # Ensure 'Python' category exists
        c = Category.objects.get(name='Python')
        response = self.client.get(reverse('rango:show_category', args=[c.slug]))
        self.assertEqual(response.status_code, 200, "Category view returned a non-200 status code.")
        self.assertContains(response, c.name, msg_prefix="Category name not found in response.")
        self.assertContains(response, "Official Python Tutorial", msg_prefix="Page title not found in response.")

    def test_category_view_not_found(self):
        """
        Check if the category view handles non-existent categories gracefully.
        """
        response = self.client.get(reverse('rango:show_category', args=['non-existent-category']))
        self.assertEqual(response.status_code, 200, "Category view returned a non-200 status code for non-existent category.")
        self.assertContains(response, "The specified category does not exist", msg_prefix="Error message not found for non-existent category.")

if __name__ == '__main__':
    unittest.main()