from rest_framework.permissions import BasePermission

class CanViewAnalyticsReport(BasePermission):
    """Allows admins and traders to view analytics reports."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'trader'] # SalesReps maybe also? Adjust as needed