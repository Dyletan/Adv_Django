from rest_framework.permissions import BasePermission

class CanManageProduct(BasePermission):
    """Allows admins and traders to manage products."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'trader']

class CanManageCategory(BasePermission):
    """Allows only admins to manage product categories."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class CanViewProduct(BasePermission):
    """Allows traders, sales reps, customers, and admins to view products."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'trader', 'sales_representative', 'customer']