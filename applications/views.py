from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from jobs.models import Job
from .models import Application
from .serializers import ApplicationSerializer
from accounts.permissions import IsCandidate

from rest_framework.generics import ListAPIView
from accounts.permissions import IsEmployer

from rest_framework.generics import UpdateAPIView
from .models import (
    Application,
    ApplicationStatusLog,
    Notification
)

from .serializers import ( ApplicationStatusLogSerializer,NotificationSerializer)


from django.db.models import Q

from .models import SavedJob
from .serializers import SavedJobSerializer

from profiles.models import CandidateProfile

class ApplyJobAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    def post(self, request, job_id):

        try:
            job = Job.objects.get(id=job_id)

        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if Application.objects.filter(
            candidate=request.user,
            job=job
        ).exists():

            return Response(
                {"error": "Already applied"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not request.user.candidate_profile.resume:

            return Response(
                {"error": "Upload resume first"},
                status=status.HTTP_400_BAD_REQUEST
            )

        application = Application.objects.create(
            candidate=request.user,
            job=job,
            resume_snapshot=request.user.candidate_profile.resume
        )

        serializer = ApplicationSerializer(
            application
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class ApplicationHistoryAPIView(ListAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    def get_queryset(self):

        return Application.objects.filter(
            candidate=self.request.user
        ).order_by(
            "-applied_date"
        )    
    
class JobApplicantsAPIView(ListAPIView):

    serializer_class = ApplicationSerializer

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def get_queryset(self):

        queryset = Application.objects.filter(
            job_id=self.kwargs["job_id"]
        )

        status_filter = self.request.GET.get(
            "status"
        )

        if status_filter:

            queryset = queryset.filter(
                status=status_filter
            )

        search = self.request.GET.get(
            "search"
        )

        if search:
            queryset = queryset.filter(
            Q(candidate__email__icontains=search)
    )

        return queryset.order_by(
            "-applied_date"
        )

class UpdateApplicationStatusAPIView(UpdateAPIView):

    serializer_class = ApplicationSerializer

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    queryset = Application.objects.all()

    def patch(self, request, *args, **kwargs):

        application = self.get_object()

        from jobs.models import User

        job_user = User.objects.filter(
            email=request.user.email
        ).first()

        if not job_user:

            return Response(
                {
                    "error": "Recruiter not found"
                },
                status=404
            )

        if (
            application.job.recruiter.user
            != job_user
        ):

            return Response(
                {
                    "error":
                    "You can update only applications for your jobs"
                },
                status=403
            )

        new_status = request.data.get(
            "status"
        )

        allowed_transitions = {

            "applied": [
                "shortlisted",
                "rejected"
            ],

            "shortlisted": [
                "interview",
                "rejected"
            ],

            "interview": [
                "selected",
                "rejected"
            ],

            "selected": [],

            "rejected": []
        }

        current_status = (
            application.status
        )

        if (
            new_status
            not in
            allowed_transitions[
                current_status
            ]
        ):

            return Response(
                {
                    "error":
                    f"Cannot move "
                    f"from "
                    f"{current_status} "
                    f"to "
                    f"{new_status}"
                },
                status=400
            )

        old_status = application.status

        application.status = new_status

        application.save()

        Notification.objects.create(
        candidate=application.candidate,
        message=(
        f"Your application for "
        f"{application.job.title} "
        f"has been updated to "
        f"{new_status.title()}."
    )
)

        ApplicationStatusLog.objects.create(
        application=application,
        old_status=old_status,
        new_status=new_status,
        changed_by=request.user
)

        return Response(
            ApplicationSerializer(
                application
            ).data
        )
    
class ApplicationLogAPIView(APIView):
    def get(self, request, pk):
        logs = ApplicationStatusLog.objects.filter(application_id=pk)
        serializer = ApplicationStatusLogSerializer(logs, many=True)
        return Response(serializer.data)    
    

class CandidateDashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    def get(self, request):

        applications = Application.objects.filter(
            candidate=request.user
        )

        applied_jobs = applications.count()

        shortlisted = applications.filter(
            status="shortlisted"
        ).count()

        interviews = applications.filter(
            status="interview"
        ).count()

        selected = applications.filter(
            status="selected"
        ).count()

        return Response({
            "applied_jobs": applied_jobs,
            "shortlisted": shortlisted,
            "interviews": interviews,
            "selected": selected
        })
    
class SaveJobAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    def post(self, request, job_id):

        try:
            job = Job.objects.get(id=job_id)

        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found"},
                status=404
            )

        saved_job, created = SavedJob.objects.get_or_create(
            candidate=request.user,
            job=job
        )

        if not created:
            return Response(
                {"message": "Job already saved"}
            )

        return Response(
            SavedJobSerializer(saved_job).data,
            status=201
        )    
    
class SavedJobsAPIView(ListAPIView):

    serializer_class = SavedJobSerializer

    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    def get_queryset(self):

        return SavedJob.objects.filter(
            candidate=self.request.user
        ).order_by("-saved_at")


class RemoveSavedJobAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    def delete(self, request, job_id):

        saved_job = SavedJob.objects.filter(
            candidate=request.user,
            job_id=job_id
        ).first()

        if not saved_job:
            return Response(
                {"error": "Saved job not found"},
                status=404
            )

        saved_job.delete()

        return Response(
            {"message": "Job removed from saved jobs"}
        )        
    
class JobRecommendationAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    def get(self, request):

        try:
            profile = CandidateProfile.objects.get(
                user=request.user
            )

        except CandidateProfile.DoesNotExist:
            return Response(
                {"error": "Candidate profile not found"},
                status=404
            )

        candidate_skills = [
            skill.strip().lower()
            for skill in profile.skills.split(",")
        ]

        jobs = Job.objects.filter(status=True)

        recommendations = []

        for job in jobs:

            job_skills = [
                skill.strip().lower()
                for skill in job.skills.split(",")
            ]

            matched = list(
                set(candidate_skills) &
                set(job_skills)
            )

            missing = list(
                set(job_skills) -
                set(candidate_skills)
            )

            if matched:
                match_percentage = int(
                    (len(matched) / len(job_skills)) * 100
                )

                recommendations.append({
                "job_id": job.id,
                "title": job.title,
                "company": str(job.recruiter),
                "matched_skills": matched,
                "missing_skills": missing,
                "match_percentage": match_percentage
            })

        recommendations.sort(
            key=lambda x: x["match_percentage"],
            reverse=True
        )

        return Response(recommendations)    
    
class NotificationAPIView(ListAPIView):

    serializer_class = NotificationSerializer

    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    def get_queryset(self):

        return Notification.objects.filter(
            candidate=self.request.user
        ).order_by("-created_at")    