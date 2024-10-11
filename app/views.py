from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, aauthenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *


# Create your views here.
def home_view(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        user_data_has_error = False

        # Validating if the email and the username is being used by another user
        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "Username already used")

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already used")

        # Checking is passwords matched
        if password != password2:
            user_data_has_error = True
            messages.error(request, "passwords doesn't match")

        # Checking if the users password is not less that 8 characters
        if len(password) < 8:
            user_data_has_error = True
            messages.error(request, "password should not be less than 8 characters ")

        if user_data_has_error:
            return redirect('register')
        else:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                password2=password2
            )
            messages.success(request, "Account created successfully")
            return redirect('login')

        
    return render(request, 'register.html')

def login_view(request):
    return render(request, 'login.html')