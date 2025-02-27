# products/models.py
from django.db import models
from django.conf import settings # to link to User model

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE) # Seller is the User who created the listing
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products') # Optional Category
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_approval')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name