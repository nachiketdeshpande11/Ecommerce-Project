# urls.py
from django.urls import path
from . import views
from .views import ContactView

urlpatterns = [
    path('',views.home, name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('category/', views.category, name='category'),
    path('password_reset/', views.password_reset, name='password_reset'),
]