from django.urls import path
from .views import JobCreateView, JobListView, ApplyJobView

urlpatterns = [
    path('create/', JobCreateView.as_view(), name='job-create'),
    path('', JobListView.as_view(), name='job-list'),
    path('<int:job_id>/apply/', ApplyJobView.as_view(), name='job-apply'),
]