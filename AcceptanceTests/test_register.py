from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class RegisterViewTests(TestCase):

    def setUp(self):
        # Create a user for testing
        self.username = "existinguser"
        self.email = "existinguser@example.com"
        self.password = "Testpassword1!"
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_register_view_get(self):
        # Test GET request to register view
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_view_post_success(self):
        # Test successful POST request to register view
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "Testpassword1!",
            "password2": "Testpassword1!"
        })
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_view_post_passwords_do_not_match(self):
        # Test POST request with passwords that do not match
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "Testpassword1!",
            "password2": "Differentpassword1!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Passwords do not match.")

    def test_register_view_post_username_taken(self):
        # Test POST request with a username that is already taken
        response = self.client.post(reverse("register"), {
            "username": self.username,
            "email": "newuser@example.com",
            "password1": "Testpassword1!",
            "password2": "Testpassword1!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username already taken.")

    def test_register_view_post_invalid_email(self):
        # Test POST request with various invalid emails
        invalid_emails = [
            "plainaddress",
            "@missingusername.com",
            "username@.com",
            "username@com",
            "username@domain..com",
            "username@domain.c",
            "username@domain.toolongtld"
        ]
        for email in invalid_emails:
            response = self.client.post(reverse("register"), {
                "username": "newuser",
                "email": email,
                "password1": "Testpassword1!",
                "password2": "Testpassword1!"
            })
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "register.html")
            messages = list(response.wsgi_request._messages)
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), "Invalid email.")

    def test_register_view_post_email_taken(self):
        # Test POST request with an email that is already registered
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": self.email,
            "password1": "Testpassword1!",
            "password2": "Testpassword1!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email is already registered.")

    def test_register_view_post_invalid_password(self):
        # Test POST request with various invalid passwords
        invalid_passwords = {
            "short": "Short1!",
            "no_uppercase": "testpassword1!",
            "no_lowercase": "TESTPASSWORD1!",
            "no_number": "Testpassword!",
            "no_symbol": "Testpassword1"
        }
        for reason, password in invalid_passwords.items():
            response = self.client.post(reverse("register"), {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": password,
                "password2": password
            })
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "register.html")
            messages = list(response.wsgi_request._messages)
            self.assertEqual(len(messages), 1)
            self.assertIn("Password", str(messages[0]))