from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginViewTests(TestCase):

    def setUp(self):
        # Create a user for testing
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_view_get(self):
        # Test GET request to login view
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_view_post_success(self):
        # Test successful POST request to login view
        response = self.client.post(reverse("login"), {
            "username": self.username,
            "password": self.password
        })
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_invalid_credentials(self):
        # Test POST request with invalid credentials
        response = self.client.post(reverse("login"), {
            "username": self.username,
            "password": "wrongpassword"
        })
        self.assertRedirects(response, reverse("login"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid username or password.")