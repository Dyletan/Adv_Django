from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username') # Display username

    class Meta:
        model = Notification
        fields = '__all__'