from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import Http404
from django.core.mail import send_mail
from .models import User, JobSeekerProfile
from .serializers import RegisterSerializer, LoginSerializer, JobSeekerProfileSerializer
from resumes.parser import parse_resume
from analytics.models import LogEntry

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Send verification email
            subject = 'Verify Your Email'
            message = f'Click this link to verify: http://localhost:8000/api/auth/verify/{user.verification_uuid}/'
            send_mail(
                subject,
                message,
                'eldar1016@gmail.com',
                [user.email],
                fail_silently=False,
            )
            LogEntry.objects.create(
                user_id=str(user.id),
                action="register",
                details=f"Registered as {user.role}"
            )
            return Response({"message": "User registered, please verify your email"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.data['email'], password=serializer.data['password'])
            if user and user.is_verified:
                refresh = RefreshToken.for_user(user)
                LogEntry.objects.create(
                    user_id=str(user.id),
                    action="login",
                    details="User logged in"
                )
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({"error": "Invalid credentials or email not verified"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request, uuid):
        try:
            user = User.objects.get(verification_uuid=uuid)
            if user.is_verified:
                return Response({"message": "Email already verified"}, status=status.HTTP_200_OK)
            user.is_verified = True
            user.verification_uuid = None
            user.save()
            LogEntry.objects.create(
                user_id=str(user.id),
                action="verify_email",
                details="Email verified"
            )
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise Http404("Verification link is invalid or expired")

class ResumeUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'job_seeker':
            return Response({"error": "Only Job Seekers can upload resumes"}, status=status.HTTP_403_FORBIDDEN)
        serializer = JobSeekerProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = JobSeekerProfile.objects.create(user=request.user, **serializer.validated_data)
            try:
                parsed_resume = parse_resume(profile.resume.path, str(request.user.id))
                LogEntry.objects.create(
                    user_id=str(request.user.id),
                    action="upload_resume",
                    details=f"Uploaded resume: {profile.resume.name}"
                )
                return Response({"message": "Resume uploaded and parsed successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Failed to parse resume: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobSeekerProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = JobSeekerProfile.objects.filter(user=request.user)
        serializer = JobSeekerProfileSerializer(profiles, many=True)
        return Response(serializer.data)