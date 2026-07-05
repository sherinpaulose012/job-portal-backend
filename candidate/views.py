from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .serializers import ResumeUploadSerializer

from .utils import (
    extract_resume_text,
    clean_resume_text,
)

class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = ResumeUploadSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            resume = serializer.save()

            text = extract_resume_text(
            resume.file.path
        )
            cleaned = clean_resume_text(text)

            return Response(
    {
        "message": "Resume uploaded successfully",

        "resume": resume.file.url,

        "extracted_text": cleaned
    },
    status=201
)

        return Response(serializer.errors, status=400)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from profiles.models import CandidateProfile
from jobs.models import Job

from .ats import calculate_ats_score


class ATSMatchAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):

        profile = CandidateProfile.objects.get(
            user=request.user
        )

        job = Job.objects.get(
            id=job_id
        )

        result = calculate_ats_score(
            profile.parsed_resume,
            job
        )

        return Response(result)    
    

