from rest_framework.permissions import BasePermission

class CanPlaceOrder(BasePermission):
    """Allows traders and customers to place orders."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['trader', 'customer']

class CanViewOrder(BasePermission):
    """Allows traders, customers (their own orders), and admins to view orders."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'trader', 'customer']

class IsOrderOwnerOrAdmin(BasePermission):
    """Allows order owner or admin to access order details."""
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (obj.user == request.user or request.user.role == 'admin')

class CanViewTransaction(BasePermission):
    """Allows traders and admins to view transactions."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'trader']