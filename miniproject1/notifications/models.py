from django.db import models
from django.conf import settings

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('trade_executed', 'Trade Executed'),
        ('sales_order_update', 'Sales Order Update'),
        ('general_info', 'General Information'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.notification_type} - {self.timestamp}"