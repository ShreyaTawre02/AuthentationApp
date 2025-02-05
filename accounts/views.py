from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from auth_project import settings
from .forms import SignupForm, LoginForm
from .models import CustomUser
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
User = get_user_model()
# Signup View
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("email")  # Use email as username
            if User.objects.filter(username=username).exists():
                messages.error(request, "A user with this email already exists. Please log in.")
                return redirect("signup")  # Redirect back to signup page
            user = form.save(commit=False)
            user.username = username  # Ensure username is the same as email
            user.is_active = False  # Ensure email verification
            user.save()
            
             # Send verification email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            verification_url = request.build_absolute_uri(
                f"/verify/{uid}/{token}/"
            )

            # Compose email subject and message
            subject = "Activate Your Account"
            message = render_to_string("accounts/activation_email.html", {
                'user': user,
                'verification_url': verification_url
            })

            # Send email using the settings
            send_mail(
                subject, 
                message, 
                settings.EMAIL_HOST_USER,  # Use the email from settings
                [user.email]
            )

            messages.success(request, "A verification email has been sent. Please check your inbox.")
            return redirect('login')
        else:
            messages.error(request, "Invalid form submission. Please correct the errors.")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


# Verify Email
def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated successfully!")
            return redirect('login')
        else:
            messages.error(request, "The activation link is invalid or has expired.")
            return redirect('login')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "The activation link is invalid or has expired.")
        return redirect('login')
@login_required
def truncate_users(request):
    # Check if the user is an admin or has the right permissions
  
    # Truncate the CustomUser table
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM accounts_customuser;")

    return redirect('home') 

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:  # Check if email is verified
                login(request, user)
                messages.success(request, "Login successful! Welcome back.")
                return redirect('about')
            else:
                messages.error(request, "Please verify your email first.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# About Page (Only accessible after login)
@login_required
def about_view(request):
    return render(request, 'accounts/about.html')

def home(request):
    users = User.objects.values("username", "email", "mobile")  # Fetch users without passwords
    return render(request, "accounts/home.html", {"users": users})
