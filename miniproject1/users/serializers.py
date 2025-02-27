from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile_image', 'first_name', 'last_name'] # Include necessary fields
        extra_kwargs = {
            'password': {'write_only': True} # Password should not be read in API responses
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None) # Handle password updates separately
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user