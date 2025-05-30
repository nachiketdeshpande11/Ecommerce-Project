# admin.py
from django.contrib import admin
from ecommerce_app.models import Contact, Product, Cart, Order
# Register your models here.

admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)