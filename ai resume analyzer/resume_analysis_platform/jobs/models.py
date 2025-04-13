from django.db import models
from accounts.models import User, JobSeekerProfile
from django.core.validators import MaxValueValidator, MinValueValidator

class SkillTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'skill_tags'

    def __str__(self):
        return self.name

class JobListing(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'recruiter'})
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=20, choices=[('remote', 'Remote'), ('hybrid', 'Hybrid'), ('onsite', 'Onsite')])
    required_experience = models.PositiveIntegerField()
    required_skills = models.ManyToManyField(SkillTag)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'job_listings'

    def __str__(self):
        return self.title

class Application(models.Model):
    job_seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    job_listing = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    resume_used = models.FileField(upload_to='resumes/')
    feedback_text = models.TextField(blank=True)
    match_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'applications'

    def __str__(self):
        return f"{self.job_seeker.user.email} - {self.job_listing.title}"