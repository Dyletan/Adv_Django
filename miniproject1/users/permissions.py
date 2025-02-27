from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Allows access only to admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsTrader(BasePermission):
    """Allows access to admin and trader users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'trader']

class IsCustomer(BasePermission):
    """Allows access to admin, sales representative, trader, and customer users.
    Note: Customer role might have limited access depending on context."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['customer', 'trader', 'admin']

class IsAdminOrSelf(BasePermission):
    """Allows admin users to manage all, and users to manage their own profiles."""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (request.user.role == 'admin' or obj == request.user)