from django.db import models

class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]
    
    transaction = models.OneToOneField('trading.Transaction', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"SalesOrder {self.id} - {self.transaction.buy_order.product.name}"

class Invoice(models.Model):
    sales_order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.id} - {self.sales_order.transaction.buy_order.product.name}"