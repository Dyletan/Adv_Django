from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission # Import Group and Permission

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('trader', 'Trader'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    profile_image = models.ImageField(upload_to='profile_pictures/', null=True, blank=True) # For profile image upload

    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="sales_trading_user_set", # Add a unique related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="sales_trading_user_set", # Add a unique related_name
        related_query_name="user",
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        ordering = ['id']