from accounts.models import JobSeekerProfile
from django.core.files import File
from django.contrib.auth import get_user_model
user = get_user_model().objects.get(email="test@example.com")
with open("media/resumes/test_resume.pdf", "rb") as f:
    profile = JobSeekerProfile.objects.create(user=user, resume=File(f, name="test_resume.pdf"))