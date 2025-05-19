# views.py
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db import IntegrityError, DatabaseError
from django.contrib import messages
from django.shortcuts import redirect
from .models import Contact


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
    
import re
from django.contrib.auth.models import User
def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirmPassword')

            # Validate username
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
            
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "Database error: A duplicate entry might exist.")
        except DatabaseError:
            messages.error(request, "Database error: Please try again later.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')
