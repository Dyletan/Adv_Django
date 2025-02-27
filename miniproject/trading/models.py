# trading/models.py
from django.db import models
from django.conf import settings # to link to User model
from products.models import Product # to link to Product model

class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('executed', 'Executed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE) # User who placed the order
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE) # Product being ordered
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_type.capitalize()} Order #{self.id} for {self.quantity} {self.product.name} by {self.user.username}"

class Transaction(models.Model):
    payment_status_choices = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    buy_order = models.ForeignKey(Order, related_name='transactions_bought', on_delete=models.CASCADE)
    sell_order = models.ForeignKey(Order, related_name='transactions_sold', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=payment_status_choices, default='pending')
    
    def __str__(self):
        return f"Transaction #{self.id} - Buy Order: {self.buy_order.id}, Sell Order: {self.sell_order.id}, Qty: {self.quantity}, Price: {self.price}"
