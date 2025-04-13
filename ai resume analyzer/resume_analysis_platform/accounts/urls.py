from django.urls import path
from .views import RegisterView, LoginView, VerifyEmailView, ResumeUploadView, JobSeekerProfileListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify/<uuid:uuid>/', VerifyEmailView.as_view(), name='verify-email'),  # New route
    path('upload-resume/', ResumeUploadView.as_view(), name='upload-resume'),
    path('profiles/', JobSeekerProfileListView.as_view(), name='profiles'),
]