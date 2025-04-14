from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.verification_uuid = uuid.uuid4()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=[('job_seeker', 'Job Seeker'), ('recruiter', 'Recruiter'), ('admin', 'Admin')],
        default='job_seeker'
    )
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    verification_uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    class Meta:
        db_table = 'users'

class JobSeekerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'job_seeker'})
    location = models.CharField(max_length=100, blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    class Meta:
        db_table = 'job_seeker_profiles'
        
class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'recruiter'})
    company_name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'recruiter_profiles'