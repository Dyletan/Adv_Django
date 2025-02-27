from rest_framework import permissions

class IsOrderOwnerOrAdminOrSalesRep(permissions.BasePermission):
    """
    Permission to allow order owner, admin, or sales_rep to view order details.
    """
    def has_object_permission(self, request, view, obj):
        # Order owner can view
        if obj.user == request.user:
            return True

        # Admin or Sales Rep can view all order details
        return request.user.is_staff or request.user.role == 'sales_rep'