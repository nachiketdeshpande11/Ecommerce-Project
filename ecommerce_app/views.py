# views.py
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db import IntegrityError, DatabaseError
from django.contrib import messages
from django.shortcuts import redirect
from .models import Contact
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
import re
from django.conf import settings
from django.core.mail import send_mail
import random
from django.utils.timezone import now
from datetime import timedelta



# Create your views here.
def home(request):
    return render(request, 'home.html')

# def contact(request):
#     return render(request, 'contact.html')

@method_decorator(csrf_protect, name='dispatch')
class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            name = request.POST.get('name', '').strip()
            contact = request.POST.get('contact', '').strip()
            email = request.POST.get('email', '').strip()
            description = request.POST.get('description', '').strip()

            errors = []
            if not name:
                errors.append("Name is required.")
            if not contact.isdigit() or len(contact) != 10:
                errors.append("Contact must be 10 digits.")
            if "@" not in email or "." not in email:
                errors.append("Email must be valid.")
            if not description:
                errors.append("Description is required.")

            if errors:
                for error in errors:
                    messages.error(request, error)
                return render(request, self.template_name)

            Contact.objects.create(
                name=name,
                contact=contact,
                email=email,
                description=description
            )

            messages.success(request, "Your message has been sent successfully.")
            return redirect('contact')

        except IntegrityError:
            messages.error(request, "Database error: A duplicate entry might exist.")
        except DatabaseError:
            messages.error(request, "Database error: Please try again later.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

        return render(request, self.template_name)

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirmPassword')

            if not username or not email or not password or not confirmPassword:
                messages.error(request, "All fields are required.")
                return render(request, 'register.html')

            if password != confirmPassword:
                messages.error(request, "Passwords do not match.")
                return render(request, 'register.html')

            if len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
                return render(request, 'register.html')

            if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
                messages.error(request, "Password must contain both letters and numbers.")
                return render(request, 'register.html')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, 'register.html')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return render(request, 'register.html')


            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            subject = 'Welcome to Our E-commerce Site'
            message = f'''
Hi {username},
Welcome to ECOMMERCE!
We're excited to have you join our community. Your registration was successful, and your account is now active. You can start exploring our wide range of products and enjoy a seamless shopping experience.

If you have any questions or need assistance, feel free to reach out to our support team.
Thank you for choosing ECOMMERCE. Happy shopping!

Best regards,
The ECOMMERCE Team
            '''
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')

        except IntegrityError:
            messages.error(request, "Database error: A duplicate entry might exist.")
        except DatabaseError:
            messages.error(request, "Database error: Please try again later.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

    return render(request, 'register.html')

# login view
from django.contrib.auth import authenticate, login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "Logout successful.")
    return redirect('login')

def category(request):
    return render(request, 'category.html')


otp_storage = {}
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            otp_storage[email] = {"otp": otp, "time": now()}

            request.session["reset_email"] = email 

            subject = "Password Reset OTP - Ecommerce"
            message = f"""
Hello {user.username},
You requested a password reset. Use the OTP below to proceed:

Your OTP: {otp}

This OTP is valid for 10 minutes.

If you didn't request this, please ignore this email.

Regards,
Ecommerce Team
"""
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            messages.success(request, "OTP has been sent to your email.")
            return redirect("verify_otp")

        except User.DoesNotExist:
            messages.error(request, "Email not registered.")
            return redirect("forgot_password")

    return render(request, "forgot_password.html")


def verify_otp(request):
    if request.method == "POST":
        email = request.session.get("reset_email", "").strip().lower()
        otp_entered = request.POST.get("otp")

        if email in otp_storage:
            otp_data = otp_storage[email]

            if now() - otp_data["time"] > timedelta(minutes=10):
                del otp_storage[email]
                messages.error(request, "OTP has expired. Please request a new one.")
                return redirect("forgot_password")

            if str(otp_entered) == str(otp_data["otp"]):
                messages.success(request, "OTP verified successfully.")
                return redirect("/")  
            else:
                messages.error(request, "Invalid OTP.")
                return redirect("verify_otp")
        else:
            messages.error(request, "OTP expired or not found. Please try again.")
            return redirect("forgot_password")

    return render(request, "verify_otp.html")
