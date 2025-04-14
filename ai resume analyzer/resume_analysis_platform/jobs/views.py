from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import JobListing, Application
from .serializers import JobListingSerializer, ApplicationSerializer
from accounts.models import JobSeekerProfile
from resumes.models import ParsedResume
from analytics.models import LogEntry
import spacy

nlp = spacy.load("en_core_web_md")

class JobCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'recruiter':
            return Response({"error": "Only recruiters can create jobs"}, status=status.HTTP_403_FORBIDDEN)
        serializer = JobListingSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save(recruiter=request.user)
            LogEntry.objects.using('analytics').create(
                user_id=str(request.user.id),
                action="create_job",
                details=f"Created job: {job.title} at {job.company_name} (ID: {job.id})"
            )
            return Response({"message": "Job created successfully", "job": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class JobListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        jobs = JobListing.objects.all()
        serializer = JobListingSerializer(jobs, many=True)
        return Response(serializer.data)

class JobDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, job_id):
        try:
            job = JobListing.objects.get(id=job_id)
            serializer = JobListingSerializer(job)
            return Response(serializer.data)
        except JobListing.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

class ApplyJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        if request.user.role != 'job_seeker':
            return Response({"error": "Only job seekers can apply"}, status=status.HTTP_403_FORBIDDEN)
        try:
            job = JobListing.objects.get(id=job_id)
            profile = JobSeekerProfile.objects.filter(user=request.user).latest('id')
            parsed_resume = ParsedResume.objects.filter(user_id=str(request.user.id)).order_by('-created_at').first()
        except (JobListing.DoesNotExist, JobSeekerProfile.DoesNotExist, ParsedResume.DoesNotExist):
            return Response({"error": "Job, profile, or resume not found"}, status=status.HTTP_404_NOT_FOUND)

        # Simple match scoring using spaCy
        resume_text = parsed_resume.text
        job_text = f"{job.title} {job.description} {' '.join(skill.name for skill in job.required_skills.all())}"
        resume_doc = nlp(resume_text)
        job_doc = nlp(job_text)
        match_score = round(resume_doc.similarity(job_doc) * 10, 1)

        # Basic feedback
        feedback = "Your resume aligns well with the job requirements."

        application = Application.objects.create(
            job_seeker=profile,
            job_listing=job,
            resume_used=profile.resume,
            feedback_text=feedback,
            match_score=match_score
        )
        LogEntry.objects.using('analytics').create(
            user_id=str(request.user.id),
            action="apply_job",
            details=f"Applied to job: {job.title} (ID: {job.id})"
        )
        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)