# products/permissions.py
from rest_framework import permissions

class IsSellerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Permission to allow sellers/admins to create, update, delete,
    and read-only access for everyone else.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # Read permissions are allowed to any request,
            return True

        # Write permissions are allowed to authenticated users with 'trader' role or admin
        return request.user and (request.user.role == 'trader' or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # Read permissions are allowed to any request,
            return True

        # Instance-level write permissions are only allowed if the user is the seller or admin
        return obj.seller == request.user or request.user.is_staff


class IsSellerOrAdmin(permissions.BasePermission): # For actions that require Seller or Admin, but not read-only
    """
    Permission to allow sellers and admins full access, but no access for others.
    (Example - not directly used in products views now, but can be used elsewhere if needed)
    """
    def has_permission(self, request, view):
        return request.user and (request.user.role == 'trader' or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.role == 'trader' or request.user.is_staff)