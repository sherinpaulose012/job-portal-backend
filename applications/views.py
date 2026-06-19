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
    ApplicationStatusLog
)

from .serializers import ApplicationStatusLogSerializer

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

        return Application.objects.filter(
            job_id=self.kwargs["job_id"]
        ).order_by(
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