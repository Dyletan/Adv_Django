from django.urls import path
from .views import RegisterView, LoginView, VerifyEmailView, JobSeekerProfileListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify/<uuid:uuid>/', VerifyEmailView.as_view(), name='verify-email'),
    path('profiles/', JobSeekerProfileListView.as_view(), name='profiles'),
]