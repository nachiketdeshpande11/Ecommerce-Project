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
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/',views.reset_password,name='reset_password'),

    path('category/', views.category, name='category'),
    path('product_detail/<int:pid>/', views.category_detail, name='product_detail'),
    path("catfilter/<str:cv>/", views.catfilter, name="catfilter"),
    path("sortfilter/<str:sv>/", views.sortfilter, name="sortfilter"),
    path("pricefilter/", views.pricefilter, name="pricefilter"),
    path('srcfilter/', views.srcfilter, name='srcfilter'),

    path('addtocart/<int:pid>/', views.add_to_cart, name='addtocart'),
    path('cart/', views.cart, name='cart'),
    path("updateqty/<str:x>/<int:cid>/", views.updateqty, name='updateqty'),
    path("remove/<int:cid>/", views.remove, name='remove'),

    path("placeorder/", views.placeorder, name="placeorder"),
    path("fetchorder/", views.fetchorder, name="fetchorder"),

    path("makepayment/", views.makepayment, name="makepayment"),
    path("paymentsuccess/", views.paymentsuccess, name="payment-success"),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]