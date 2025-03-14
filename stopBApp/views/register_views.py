from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
import re

class Register(View):

    def get(self, request):
        return render(request, "register.html")
    
    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            password_validation = validatePassword(password1)
            email_validation = validateEmail(email)
            if not email_validation:
                messages.error(request, "Invalid email.")
            else:
                if all(password_validation.values()):
                    if User.objects.filter(email=email).exists():
                        messages.error(request, "Email is already registered.")
                    else:
                        # Create the user
                        user = User.objects.create_user(username=username, email=email, password=password1)
                        messages.success(request, "Account created! You can now log in.")
                        return redirect("login")
                else:
                    for requirement, passed in password_validation.items():
                        if not passed:
                            messages.error(request, requirement)
                            
        return render(request, "register.html", {
            "username": username,
            "email": email
        })
        

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




    

