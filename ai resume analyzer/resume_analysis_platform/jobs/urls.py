from django.urls import path
from .views import JobCreateView, JobListView, ApplyJobView, JobDetailView

urlpatterns = [
    path('create/', JobCreateView.as_view(), name='job-create'),
    path('', JobListView.as_view(), name='job-list'),
    path('<int:job_id>/apply/', ApplyJobView.as_view(), name='job-apply'),
    path('<int:job_id>/', JobDetailView.as_view(), name='job-detail'),
]