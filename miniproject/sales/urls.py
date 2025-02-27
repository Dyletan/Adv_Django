from django.urls import path
from .views import *

urlpatterns = [
    path('', SalesOrderListView.as_view(), name='sales-order-list'),
    path('create/<int:transaction_id>/', CreateSalesOrderView.as_view(), name='create-sales-order'),
    path('<int:sales_order_id>/generate_invoice/', GenerateInvoiceView.as_view(), name='generate-invoice'),
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/<int:invoice_id>/pay/', PayInvoiceView.as_view(), name='pay-invoice'),
]