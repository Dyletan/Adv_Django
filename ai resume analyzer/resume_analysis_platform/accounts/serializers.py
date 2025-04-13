from rest_framework import serializers
from django.core.mail import send_mail
from uuid import uuid4
from .models import User, JobSeekerProfile, RecruiterProfile

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        token = str(uuid4())
        # Simplified: Store token in a model or cache later
        send_mail(
            'Verify Your Email',
            f'Click this link to verify: http://localhost:8000/api/auth/verify/{token}/',
            'from@example.com',
            [user.email],
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = ('location', 'years_experience', 'education', 'resume')