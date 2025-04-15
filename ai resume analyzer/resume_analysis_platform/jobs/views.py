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
from spacy.matcher import PhraseMatcher

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

        # Initialize spaCy matcher for skills
        matcher = PhraseMatcher(nlp.vocab)
        required_skills = [skill.name for skill in job.required_skills.all()]
        patterns = [nlp(skill.lower()) for skill in required_skills]
        matcher.add("SKILLS", patterns)

        # Process resume and job
        resume_doc = nlp(parsed_resume.text.lower())
        job_text = f"{job.title} {job.description} {' '.join(required_skills)}".lower()
        job_doc = nlp(job_text)

        # Find skill matches
        matches = matcher(resume_doc)
        matched_skills = set()
        for match_id, start, end in matches:
            skill = resume_doc[start:end].text
            matched_skills.add(skill.title())

        # Calculate match score: 70% skills, 30% general similarity
        skill_score = (len(matched_skills) / max(len(required_skills), 1)) * 7.0  # Max 7 points
        general_score = resume_doc.similarity(job_doc) * 3.0  # Max 3 points
        match_score = round(skill_score + general_score, 1)
        match_score = min(match_score, 9.5)  # Cap to avoid overly high scores

        # Generate dynamic feedback
        feedback_parts = []
        if matched_skills:
            feedback_parts.append(f"Strong match in: {', '.join(matched_skills)}.")
        missing_skills = [s.title() for s in required_skills if s.lower() not in [m.lower() for m in matched_skills]]
        if missing_skills:
            feedback_parts.append(f"Consider developing: {', '.join(missing_skills)}.")
        if match_score < 6.0:
            feedback_parts.append("Your experience may not fully align; highlight relevant projects.")
        feedback = " ".join(feedback_parts) or "Your resume shows some alignment with the role."

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

class RecruiterApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'recruiter':
            return Response({"error": "Only recruiters can view applications"}, status=status.HTTP_403_FORBIDDEN)
        
        job_id = request.query_params.get('job_id')
        applications = Application.objects.filter(job_listing__recruiter=request.user)
        if job_id:
            applications = applications.filter(job_listing__id=job_id)
        
        applications = applications.order_by('-match_score')
        data = [
            {
                'job_title': app.job_listing.title,
                'user_email': app.job_seeker.user.email,
                'resume_text': ParsedResume.objects.filter(user_id=str(app.job_seeker.user.id)).order_by('-created_at').first().text,
                'match_score': app.match_score,
                'feedback_text': app.feedback_text,
                'created_at': app.created_at
            }
            for app in applications
        ]
        return Response(data)