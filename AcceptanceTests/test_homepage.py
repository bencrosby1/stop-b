from django.test import TestCase
from django.urls import reverse

class HomepageTests(TestCase):

    def test_homepage_status_code(self):

        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_uses_correct_template(self):

        response = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'home.html')
