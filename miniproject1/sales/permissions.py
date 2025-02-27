from rest_framework.permissions import BasePermission

class CanManageSalesOrder(BasePermission):
    """Allows admins and sales representatives to manage sales orders."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'sales_representative']

class IsSalesOrderSalesRepOrAdmin(BasePermission):
    """Allows sales order's sales rep or admin to access sales order details."""
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (obj.sales_representative == request.user or request.user.role == 'admin')

class CanViewSalesOrder(BasePermission):
    """Allows sales reps (their own), customers (their own), and admins to view sales orders."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'sales_representative', 'customer']

class CanManageInvoice(BasePermission):
    """Allows only admins to manage invoices."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class CanViewInvoice(BasePermission):
    """Allows sales reps, customers (related invoices), and admins to view invoices."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'sales_representative', 'customer']

class IsInvoiceRelatedToUser(BasePermission):
    """Checks if the invoice is related to the requesting user (customer or sales rep) or if user is admin."""
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (obj.sales_order.customer == request.user or obj.sales_order.sales_representative == request.user or request.user.role == 'admin')