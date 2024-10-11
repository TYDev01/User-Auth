from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *


# Create your views here.
@login_required
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
            )
            messages.success(request, "Account created successfully")
            return redirect('login')

        
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "username or password incorrect")
            return redirect('login')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            messages.success(request, f"User with the email '{email}' found")
            new_password = PasswordReset(user=user)
            new_password.save()
            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password.reset_id})
            full_password_reset_url = f"{request.scheme}://{request.get_host()}{password_reset_url}"
            email_body = f"Reset your password using the link below: \n\n\n{full_password_reset_url}"
            email_message = EmailMessage(
                'Reset Your Password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent')
        except User.DoesNotExist:
            messages.error(request, f"User with the email '{email}' not found")

    return render(request, 'forgot.html')


def password_reset_sent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'passwordresetsent.html')
    else:
        messages.error(request, 'Invalid resed ID')
        return redirect('forgot')


def password_reset(request, reset_id):
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            password_have_errors = False

            if password != confirm_password:
                password_have_errors = True
                messages.error(request, "passwords dosen't match")
            
            if len(password) < 8:
                password_have_errors = True
                messages.error(request, "password shouldn't be less than 8 characters")

            expiration_time = password_reset_id.created_on + timezone.timedelta(minutes=10)
            if timezone.now() > expiration_time:
                password_have_errors = True
                messages.error(request, "Reset link has expired")
                password_reset_id.delete()

            # Reset password
            if not password_have_errors:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

            # Delete reset iD after use
                password_reset_id.delete()

            # Redirect to login
                messages.success(request, 'Password reset, login now')
                return redirect('login')
            else:
                return redirect('reset-password', reset_id=reset_id)
            

    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset ID')
        return redirect('forgot')