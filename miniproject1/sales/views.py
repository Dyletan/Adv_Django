from django.shortcuts import render, redirect
from .models import *
from .forms import SalesOrderForm
from rest_framework import viewsets, generics
from .serializers import SalesOrderSerializer, SalesOrderItemSerializer, InvoiceSerializer
from .permissions import CanManageSalesOrder, IsSalesOrderSalesRepOrAdmin, CanViewSalesOrder, CanManageInvoice, CanViewInvoice, IsInvoiceRelatedToUser

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all().order_by('-order_date')
    serializer_class = SalesOrderSerializer

    def perform_create(self, serializer):
        serializer.save(sales_representative=self.request.user)

    def get_queryset(self):
        """
        Sales Reps see their own sales orders, Customers see their own, Admin sees all.
        """
        user = self.request.user
        if user.role == 'sales_representative':
            return SalesOrder.objects.filter(sales_representative=user).order_by('-order_date')
        elif user.role == 'customer':
            return SalesOrder.objects.filter(customer=user).order_by('-order_date')
        return SalesOrder.objects.all().order_by('-order_date') # Admin sees all

    def get_permissions(self):
        """
        - list, retrieve: SalesRep (own), Customer (own), Admin (all) can view
        - create: SalesRep can create
        - update, partial_update, destroy: Admin only (for now, consider approval workflow later)
        """
        if self.action in ['create']:
            permission_classes = [CanManageSalesOrder] # SalesReps and Admins can create sales orders
        elif self.action in ['list', 'retrieve']:
            permission_classes = [CanViewSalesOrder, IsSalesOrderSalesRepOrAdmin] # View SalesOrder permission + ownership/admin check
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin] # Admin only can update/delete sales orders
        else:
            permission_classes = [CanViewSalesOrder] # Default view permission
        return [permission() for permission in permission_classes]


class SalesOrderItemViewSet(viewsets.ModelViewSet): # Permissions for SalesOrderItem - might need adjustment based on frontend
    queryset = SalesOrderItem.objects.all()
    serializer_class = SalesOrderItemSerializer
    permission_classes = [CanManageSalesOrder] # Admin and Sales reps can manage items (for now, might restrict further)


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet): # Invoices are read-only via API
    queryset = Invoice.objects.all().order_by('-invoice_date')
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        """
        Sales Reps see invoices related to their sales orders, Customers see invoices for their orders, Admin sees all.
        """
        user = self.request.user
        if user.role == 'sales_representative':
            return Invoice.objects.filter(sales_order__sales_representative=user).order_by('-invoice_date')
        elif user.role == 'customer':
            return Invoice.objects.filter(sales_order__customer=user).order_by('-invoice_date')
        return Invoice.objects.all().order_by('-invoice_date') # Admin sees all

    def get_permissions(self):
        """
        - list, retrieve: SalesRep (related), Customer (related), Admin (all) can view
        """
        return [CanViewInvoice(), IsInvoiceRelatedToUser()] # Combination of permission checks
    
def sales_order_create_view(request):
    if request.method == 'POST':
        form = SalesOrderForm(request.POST)
        if form.is_valid():
            sales_order = form.save(commit=False)
            sales_order.sales_representative = request.user # Assign current sales rep
            sales_order.save()
            return redirect('sales-order-list-html') # Redirect to sales order list
    else:
        form = SalesOrderForm()
    return render(request, 'sales/sales_order_create.html', {'form': form})

def sales_order_list_view(request):
    sales_orders = SalesOrder.objects.filter(sales_representative=request.user) # Show only sales rep's orders
    return render(request, 'sales/sales_order_list.html', {'sales_orders': sales_orders, 'user': request.user})