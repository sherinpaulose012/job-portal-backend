from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import CandidateProfile, EmployerProfile
from .serializers import CandidateProfileSerializer, EmployerProfileSerializer
from .permissions import IsOwnerOrAdmin

from .serializers import ResumeUploadSerializer

from candidate.utils import (
    extract_resume_text,
    clean_resume_text,
)
# =========================
# CANDIDATE PROFILE API
# =========================
class CandidateProfileAPIView(APIView):

    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    # CREATE
    def post(self, request):
        if request.user.role != "CANDIDATE":
            return Response({"error": "Only candidates allowed"}, status=403)

        serializer = CandidateProfileSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    # LIST or SELF PROFILE
    def get(self, request, pk=None):

        # SELF PROFILE
        if pk is None:
            profile = CandidateProfile.objects.filter(
                user=request.user,
                is_deleted=False
            ).first()

            serializer = CandidateProfileSerializer(profile)
            return Response(serializer.data)

        # BY ID
        profile = CandidateProfile.objects.get(id=pk, is_deleted=False)

        self.check_object_permissions(request, profile)

        serializer = CandidateProfileSerializer(profile)
        return Response(serializer.data)

    # UPDATE
    def put(self, request, pk):
        profile = CandidateProfile.objects.get(id=pk, is_deleted=False)

        self.check_object_permissions(request, profile)

        serializer = CandidateProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # DELETE
    def delete(self, request, pk):
        profile = CandidateProfile.objects.get(id=pk, is_deleted=False)

        self.check_object_permissions(request, profile)

        profile.is_deleted = True
        profile.save()

        return Response({"message": "Profile deleted"})


# =========================
# EMPLOYER PROFILE API
# =========================
class EmployerProfileAPIView(APIView):

    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def post(self, request):
        if request.user.role != "EMPLOYER":
            return Response({"error": "Only employers allowed"}, status=403)

        serializer = EmployerProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    def get(self, request, pk=None):

        # SELF PROFILE
        if pk is None:
            profile = EmployerProfile.objects.filter(
                user=request.user,
                is_deleted=False
            ).first()

            serializer = EmployerProfileSerializer(profile)
            return Response(serializer.data)

        # BY ID
        profile = EmployerProfile.objects.get(id=pk, is_deleted=False)

        self.check_object_permissions(request, profile)

        serializer = EmployerProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        profile = EmployerProfile.objects.get(id=pk, is_deleted=False)

        self.check_object_permissions(request, profile)

        serializer = EmployerProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        profile = EmployerProfile.objects.get(id=pk, is_deleted=False)

        self.check_object_permissions(request, profile)

        profile.is_deleted = True
        profile.save()

        return Response({"message": "Profile deleted"})
    
class ResumeUploadView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ResumeUploadSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=400
            )

        profile = CandidateProfile.objects.get(
            user=request.user
        )
        resume_replaced = False
        # Delete old resume
        if profile.resume:
            profile.resume.delete(save=False)
            resume_replaced = True

        
        profile.resume = serializer.validated_data['resume']
        profile.save()

        text = extract_resume_text(
        profile.resume.path
    )

        cleaned = clean_resume_text(text)
    

        return Response({
        "message": (
        "Resume replaced successfully"
        if resume_replaced
        else "Resume uploaded successfully"
    ),
    "resume": profile.resume.url,
    "extracted_text": cleaned
})
    

    
    

