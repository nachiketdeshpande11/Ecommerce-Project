# models.py
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=10)
    email = models.EmailField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    CATEGORY_CHOICES = (
        (1, 'Mobiles'),
        (2, 'Clothing'),
        (3, 'Home Appliances'),
        (4, 'Shoes'),
    )

    names = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    pimage = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.names
    
class Cart(models.Model):
    uid = models.ForeignKey('auth.User', on_delete=models.CASCADE,db_column='uid')
    pid = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='pid')
    qty = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.uid.username} - {self.pid.names} ({self.qty})"
    
class Order(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uid')
    pid = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='pid')
    qty = models.IntegerField(default=1)
    amt = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Order by {self.uid.username} for {self.pid.names} ({self.qty})"