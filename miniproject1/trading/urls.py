from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, TransactionViewSet, order_create_view, order_list_view

router = DefaultRouter()
router.register(r'api/orders', OrderViewSet) # API order views
router.register(r'api/transactions', TransactionViewSet) # API transaction views

urlpatterns = [
    path('api/', include(router.urls)), # API urls are prefixed with /api/
    path('orders-html/create/', order_create_view, name='order-create-html'), # HTML order create form
    path('orders-html/', order_list_view, name='order-list-html'), # HTML order list/history
]