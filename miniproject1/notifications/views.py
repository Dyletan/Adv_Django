from rest_framework import viewsets, generics
from .models import Notification
from .serializers import NotificationSerializer
from .permissions import CanViewNotification, IsNotificationRecipient

class NotificationViewSet(viewsets.ReadOnlyModelViewSet): # Notifications are read-only via API for users
    queryset = Notification.objects.all().order_by('-timestamp')
    serializer_class = NotificationSerializer
    permission_classes = [CanViewNotification, IsNotificationRecipient] # Users can view their own notifications
    # For listing, CanViewNotification will ensure authenticated, IsNotificationRecipient filters queryset

    def get_queryset(self):
        """
        Users see only their own notifications. Admin (if needed for notification management) would see all.
        For now, assuming users only see their own. Admin management of notifications not fully specified yet.
        """
        if self.request.user.is_authenticated:
            return Notification.objects.filter(user=self.request.user).order_by('-timestamp')
        return Notification.objects.none() # Or return empty queryset for unauthenticated users