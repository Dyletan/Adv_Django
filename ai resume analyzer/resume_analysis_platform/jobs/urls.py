from django.urls import path
from .views import JobCreateView, JobListView, ApplyJobView, JobDetailView, RecruiterApplicationsView

urlpatterns = [
    path('', JobListView.as_view(), name='job-list'),
    path('create/', JobCreateView.as_view(), name='job-create'),
    path('<int:job_id>/apply/', ApplyJobView.as_view(), name='job-apply'),
    path('<int:job_id>/', JobDetailView.as_view(), name='job-detail'),
    path('applications/', RecruiterApplicationsView.as_view(), name='recruiter-applications'),
]