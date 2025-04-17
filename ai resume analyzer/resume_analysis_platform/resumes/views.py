from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ParsedResume
from .parser import extract_resume_text
from analytics.models import LogEntry
from datetime import datetime

class UploadResumeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'job_seeker':
            return Response({"error": "Only job seekers can upload resumes"}, status=status.HTTP_403_FORBIDDEN)
        
        file = request.FILES.get('resume')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not file.name.endswith(('.pdf', '.docx')):
            return Response({"error": "Only PDF and DOCX files are supported"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Extract text using parser
            text = extract_resume_text(file)
            if not text.strip():
                return Response({"error": "Could not extract text from file"}, status=status.HTTP_400_BAD_REQUEST)

            # Create new ParsedResume
            user_id = str(request.user.id)
            parsed_resume = ParsedResume.objects.create(
                user_id=user_id,
                text=text,
                file_name=file.name,
                created_at=datetime.now()
            )

            LogEntry.objects.using('analytics').create(
                user_id=user_id,
                action="upload_resume",
                details=f"Uploaded resume {str(parsed_resume.id)} for user {user_id}, file: {file.name}"
            )
            return Response({
                "message": "Resume uploaded successfully",
                "resume_id": str(parsed_resume.id),
                "text_preview": text[:100],
                "file_name": file.name
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Failed to process resume: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)