from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class AccountViewsTests(TestCase):
    def setUp(self):
        # Create a main user for account update, deletion, and password change tests.
        self.user_password = "Testpassword1!"
        self.user = User.objects.create_user(
            username="testuser", 
            email="testuser@example.com", 
            password=self.user_password
        )
        # Create another user to test duplicate username/email conditions.
        self.other_user = User.objects.create_user(
            username="existinguser", 
            email="existinguser@example.com", 
            password="Testpassword1!"
        )
        # Log in as the main user.
        self.client.login(username=self.user.username, password=self.user_password)

    # --- Account View Tests ---
    def test_get_account_view(self):
        """GET request should render account.html with the correct user in context."""
        response = self.client.get(reverse("account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account.html")
        self.assertEqual(response.context["user"], self.user)

    def test_post_update_account_success(self):
        """POST request with valid new username and email should update the user and redirect."""
        new_username = "updateduser"
        new_email = "updateduser@example.com"
        response = self.client.post(reverse("account"), {
            "username": new_username,
            "email": new_email,
        })
        # Expect a redirect to "account"
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("account"))
        # Refresh the user instance and check changes.
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, new_username)
        self.assertEqual(self.user.email, new_email)

    def test_post_update_account_username_taken(self):
        """POST request should not allow updating to a username that is already taken."""
        response = self.client.post(reverse("account"), {
            "username": self.other_user.username,
            "email": "uniqueemail@example.com",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account.html")
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username is already taken.")

    def test_post_update_account_email_taken(self):
        """POST request should not allow updating to an email that is already registered."""
        response = self.client.post(reverse("account"), {
            "username": "uniqueusername",
            "email": self.other_user.email,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account.html")
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email is already registered.")

    def test_post_update_account_invalid_email(self):
        """POST request should not allow an invalid email address."""
        response = self.client.post(reverse("account"), {
            "username": "uniqueusername",
            "email": "invalid-email",  # invalid format
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account.html")
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid email.")

    # --- DeleteAccount View Tests ---
    def test_delete_account_correct_password(self):
        """POST request with correct password should delete the account and redirect to home."""
        response = self.client.post(reverse("delete_account"), {
            "password": self.user_password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))
        # The user should no longer exist.
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)

    def test_delete_account_incorrect_password(self):
        """POST request with incorrect password should not delete the account."""
        response = self.client.post(reverse("delete_account"), {
            "password": "WrongPassword!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("account"))
        # The user should still exist.
        self.assertTrue(User.objects.filter(id=self.user.id).exists())
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Incorrect password. Account not deleted.")

    # --- EditPassword View Tests ---
    def test_edit_password_incorrect_old_password(self):
        """POST request should not change password if old password is incorrect."""
        response = self.client.post(reverse("edit_password"), {
            "old_password": "WrongOldPassword",
            "new_password1": "Newpassword1!",
            "new_password2": "Newpassword1!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("account"))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Incorrect password.")

    def test_edit_password_mismatch_new_password(self):
        """POST request should not change password if the new passwords do not match."""
        response = self.client.post(reverse("edit_password"), {
            "old_password": self.user_password,
            "new_password1": "Newpassword1!",
            "new_password2": "Differentpassword1!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("account"))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "New passwords do not match.")

    def test_edit_password_invalid_new_password(self):
        """POST request should not change password if the new password doesn't meet validation requirements."""
        # Example: missing a symbol
        response = self.client.post(reverse("edit_password"), {
            "old_password": self.user_password,
            "new_password1": "Newpassword1",  # no symbol
            "new_password2": "Newpassword1",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("account"))
        messages = list(response.wsgi_request._messages)
        # Check that at least one error message mentions a password requirement.
        self.assertTrue(any("Password" in str(message) for message in messages))

    def test_edit_password_success(self):
        """POST request with correct old password and a valid new password should update the password."""
        new_password = "Newpassword1!"
        response = self.client.post(reverse("edit_password"), {
            "old_password": self.user_password,
            "new_password1": new_password,
            "new_password2": new_password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("account"))
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("Password updated successfully!" in str(message) for message in messages))
        # Refresh the user and verify that the password was updated.
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))
