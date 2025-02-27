from rest_framework.permissions import BasePermission

class CanViewNotification(BasePermission):
    """Allows all authenticated users to view their own notifications."""
    def has_permission(self, request, view):
        return request.user.is_authenticated

class IsNotificationRecipient(BasePermission):
    """Checks if the notification is for the requesting user."""
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user