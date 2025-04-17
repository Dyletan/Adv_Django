from django.urls import path
from .views import JobCreateView, JobListView, ApplyJobView, JobDetailView, RecruiterApplicationsView, MyListingsView, ResumeListView

urlpatterns = [
    path('', JobListView.as_view(), name='job-list'),
    path('create/', JobCreateView.as_view(), name='job-create'),
    path('my-listings/', MyListingsView.as_view(), name='my-listings'),
    path('<int:job_id>/apply/', ApplyJobView.as_view(), name='job-apply'),
    path('<int:job_id>/', JobDetailView.as_view(), name='job-detail'),
    path('applications/', RecruiterApplicationsView.as_view(), name='recruiter-applications'),
    path('applications/<int:job_id>/', RecruiterApplicationsView.as_view(), name='recruiter-applications-job'),
    path('resumes/', ResumeListView.as_view(), name='resume-list'),
]