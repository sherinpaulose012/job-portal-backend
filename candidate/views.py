from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .serializers import ResumeUploadSerializer


class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = ResumeUploadSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            resume = serializer.save()

            return Response({
                "message": "Resume uploaded successfully",
                "resume": resume.file.url
            }, status=201)

        return Response(serializer.errors, status=400)