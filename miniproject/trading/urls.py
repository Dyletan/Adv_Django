from django.urls import path
from .views import CreateBuyOrderView, ApproveTransactionView, CancelTransactionView, OrderListView, TransactionListView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/<int:product_id>/', CreateBuyOrderView.as_view(), name='create-buy-order'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:transaction_id>/approve/', ApproveTransactionView.as_view(), name='approve-transaction'),
    path('transactions/<int:transaction_id>/cancel/', CancelTransactionView.as_view(), name='cancel-transaction'),
]
