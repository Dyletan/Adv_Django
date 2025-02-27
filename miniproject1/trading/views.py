from django.shortcuts import render, redirect
from .models import Order, Transaction
from .forms import OrderForm
from rest_framework import viewsets, generics, permissions
from .serializers import OrderSerializer, TransactionSerializer
from .permissions import CanPlaceOrder, CanViewOrder, IsOrderOwnerOrAdmin, CanViewTransaction
from users.permissions import IsAdmin

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-timestamp')
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Customers and Traders see only their own orders, Admin sees all.
        """
        if self.request.user.role in ['customer', 'trader']:
            return Order.objects.filter(user=self.request.user).order_by('-timestamp')
        return Order.objects.all().order_by('-timestamp') # Admin sees all orders

    def get_permissions(self):
        """
        - list, retrieve: Trader, Customer (own orders), Admin (all) can view
        - create: Trader, Customer can create
        - update, partial_update, destroy: Admin only for now (consider order cancellation later)
        """
        if self.action in ['create']:
            permission_classes = [CanPlaceOrder] # Traders and Customers can create orders
        elif self.action in ['list', 'retrieve']:
            permission_classes = [CanViewOrder, IsOrderOwnerOrAdmin] # View order permission + owner or admin check for retrieve
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin] # Only admin can update/delete orders (for now)
        else:
            permission_classes = [CanViewOrder] # Default view permission
        return [permission() for permission in permission_classes]


class TransactionViewSet(viewsets.ReadOnlyModelViewSet): # Transactions are read-only
    queryset = Transaction.objects.all().order_by('-timestamp')
    serializer_class = TransactionSerializer
    permission_classes = [CanViewTransaction] # Traders and Admins can view transactions
    
def order_create_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user # Assign current user
            order.save()
            return redirect('order-list-html') # Redirect to order list after successful creation
    else:
        form = OrderForm()
    return render(request, 'trading/order_create.html', {'form': form})

def order_list_view(request):
    orders = Order.objects.filter(user=request.user) # Show only user's orders
    return render(request, 'trading/order_list.html', {'orders': orders, 'user': request.user})