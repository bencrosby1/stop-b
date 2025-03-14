from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.views import View
import re

class Account(View):
    def get(self, request):
        return render(request, "account.html", {"user": request.user})  # Ensures user data persists

    def post(self, request):
        user = request.user
        username = request.POST["username"]
        email = request.POST["email"]
        email_validation = validateEmail(email)

        # Check if username already exists (except for current user)
        if User.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, "Username is already taken.")
        elif User.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, "Email is already registered.")
        elif not email_validation:
            messages.error(request, "Invalid email.")
        else:
            # Update user details
            user.username = username
            user.email = email
            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("account")  # Redirect to home page after successful update
        
        return render(request, "account.html", {"user": user})

@login_required
def DeleteAccount(request):
    if request.method == "POST":
        password = request.POST.get("password")
        user = request.user

    # Verify password before deleting
    if authenticate(username=user.username, password=password):
        user.delete()
        messages.success(request, "Your account has been deleted.")
        logout(request)
        return redirect("home")
    else:
        messages.error(request, "Incorrect password. Account not deleted.")
        return redirect("account")  # Stay on the account page
    
@login_required
def EditPassword(request):
    if request.method == "POST":
        user = request.user
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        # Verify old password
        if not authenticate(username=user.username, password=old_password):
            messages.error(request, "Incorrect password.")
        elif new_password1 != new_password2:
            messages.error(request, "New passwords do not match.")
        else:
            validate_password = validatePassword(new_password1)
            if not all(validate_password.values()):
                for requirement, passed in validate_password.items():
                    if not passed:
                        messages.error(request, requirement)
            else:
                user.set_password(new_password1)
                user.save()
                login(request, user)
                messages.success(request, "Password updated successfully!")
    return redirect("account")  # Stay on the account page

def validatePassword(password):
    requirements = {
        "Password must be at least 8 characters long": len(password) >= 8,
        "Password must contain at least one number": any(char.isdigit() for char in password),
        "Password must contain at least one uppercase letter": any(char.isupper() for char in password),
        "Password must contain at least one lowercase letter": any(char.islower() for char in password),
        "Password must contain at least one symbol": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    }
    return requirements

def validateEmail(email):
    pattern = r'^(?!.*\.\.)[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}$'
    return bool(re.match(pattern, email))