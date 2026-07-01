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