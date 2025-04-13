from django.db import models

class LogEntry(models.Model):
    user_id = models.CharField(max_length=255, null=True, blank=True)  # Store user ID as a string
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    class Meta:
        db_table = 'log_entries'

    def __str__(self):
        return f"{self.user_id or 'Anonymous'} - {self.action}"