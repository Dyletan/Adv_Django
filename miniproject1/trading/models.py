from django.db import models
from django.conf import settings

class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('open', 'Open'),
        ('matched', 'Matched'),
        ('cancelled', 'Cancelled'),
        ('fulfilled', 'Fulfilled'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='orders')
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_type.capitalize()} {self.quantity} {self.product.name} @ {self.price} by {self.user.username} ({self.status})"

class Transaction(models.Model):
    buy_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='buy_transactions')
    sell_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sell_transactions')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    transaction_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Execution Price')
    transaction_quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction: Buy Order {self.buy_order.id}, Sell Order {self.sell_order.id}, Price: {self.transaction_price}, Qty: {self.transaction_quantity}"