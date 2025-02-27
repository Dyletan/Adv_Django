from django.db import models
from django.conf import settings
import pdfkit
from django.template.loader import render_to_string
from products.models import Product

class SalesOrder(models.Model):
    SALES_ORDER_STATUS_CHOICES = [
        ('pending_payment', 'Pending Payment'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    transaction = models.OneToOneField('trading.Transaction', on_delete=models.CASCADE, related_name='sales_order', unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales_orders_seller', verbose_name='Seller')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales_orders_customer', verbose_name='Customer')
    quantity = models.IntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Sale Price')
    status = models.CharField(max_length=20, choices=SALES_ORDER_STATUS_CHOICES, default='pending_payment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='Discount (%)')

    def __str__(self):
        return f"Sales Order #{self.id} - Transaction: {self.transaction.id}, Customer: {self.customer.username}"
    
class Invoice(models.Model):
    INVOICE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    sales_order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE, related_name='invoice', unique=True) # Corrected: OneToOne to SalesOrder
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name='Invoice Number')
    payment_status = models.CharField(max_length=10, choices=INVOICE_STATUS_CHOICES, default='pending')
    invoice_date = models.DateTimeField(auto_now_add=True, verbose_name='Invoice Date')
    original_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.get_payment_status_display()} for Sales Order #{self.sales_order.id}" # Corrected __str__ to link to SalesOrder

    @property
    def total_amount(self):
        """Calculate final amount after discount."""
        return max(self.original_amount * (1 - self.discount_percent), 0)

    def generate_pdf(self):
        """Generate a PDF invoice and save to pdf_file field.""" # Updated docstring
        context = {
            'invoice': self,
            'sales_order': self.sales_order,
            'total_amount': self.total_amount,
        }
        html_string = render_to_string('invoices/invoice_template.html', context)
        pdf = pdfkit.from_string(html_string, False)
        invoice_number_filename = f'invoice_{self.invoice_number}.pdf'
        filepath = f'invoices/{invoice_number_filename}'
        full_filepath = f'media/{filepath}'

        with open(full_filepath, 'wb') as f:
            f.write(pdf)

        self.pdf_file.name = filepath
        self.save()

        return filepath # Return the relative path to the PDF file

