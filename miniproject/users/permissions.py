from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # SAFE_METHODS are GET, HEAD, OPTIONS (read-only)
            return True
        return request.user and request.user.is_staff # is_staff usually means admin in Django

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff