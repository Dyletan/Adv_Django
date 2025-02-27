from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesOrderViewSet, SalesOrderItemViewSet, InvoiceViewSet, sales_order_create_view, sales_order_list_view

router = DefaultRouter()
router.register(r'api/sales-orders', SalesOrderViewSet) # API sales order views
router.register(r'api/sales-order-items', SalesOrderItemViewSet) # API sales order item views
router.register(r'api/invoices', InvoiceViewSet) # API invoice views

urlpatterns = [
    path('api/', include(router.urls)), # API urls are prefixed with /api/
    path('sales-orders-html/create/', sales_order_create_view, name='sales-order-create-html'), # HTML sales order create
    path('sales-orders-html/', sales_order_list_view, name='sales-order-list-html'), # HTML sales order list
]