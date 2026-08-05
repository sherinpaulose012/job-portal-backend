from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .models import Job, Recruiter,User
from .serializers import JobSerializer
from .pagination import JobPagination
from .permissions import IsEmployer

from .filters import JobFilter
from .permissions import IsRecruiter

from .throttles import AIRateThrottle

# Job List API
class JobListAPIView(ListAPIView):

    serializer_class = JobSerializer
    pagination_class = JobPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_class = JobFilter

    search_fields = [
        "title",
        "description",
        "skills",
        "location",
    ]

    def get_queryset(self):
        return (
            Job.objects
            .filter(status=True)
            .order_by("-created_at")
        )
    
#Featured jobs  
class FeaturedJobAPIView(ListAPIView):

    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.filter(
            status=True,
            is_featured=True
        )

#LatestJobs
class LatestJobAPIView(ListAPIView):

    serializer_class = JobSerializer

    def get_queryset(self):

        return (
            Job.objects
            .filter(status=True)
            .order_by("-created_at")
        )

# Job Create API
class JobCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def post(self, request):

        serializer = JobSerializer(
            data=request.data
        )

        if serializer.is_valid():

            print("REQUEST USER:", request.user)
            print("REQUEST USER TYPE:", type(request.user))
            print("REQUEST USER ID:", request.user.id)

            job_user = User.objects.filter(
                email=request.user.email
            ).first()

            if not job_user:

                return Response(
                    {
                        "error":
                        "Recruiter user not found"
                    },
                    status=404
                )

            recruiter = Recruiter.objects.get(
                user=job_user
            )

            serializer.save(
                recruiter=recruiter
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
# Job Update API
class JobUpdateAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def put(self, request, id):

        try:

            recruiter = Recruiter.objects.get(
                user__email=request.user.email
            )

            job = Job.objects.get(
                id=id,
                recruiter=recruiter
            )

        except Job.DoesNotExist:

            return Response(
                {
                    "error": "Job not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobSerializer(
            job,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def patch(self, request, id):

        try:

            recruiter = Recruiter.objects.get(
                user__email=request.user.email
            )

            job = Job.objects.get(
                id=id,
                recruiter=recruiter
            )

        except Job.DoesNotExist:

            return Response(
                {
                    "error": "Job not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        job.status = request.data.get(
            "status"
        )

        job.save()

        return Response(
            {
                "message":
                "Job activated"
                if job.status
                else "Job deactivated",

                "status": job.status
            },
            status=status.HTTP_200_OK
        )

# User Test API
class UserTestAPIView(APIView):

    def get(self, request):

        return Response(
            {
                "message": "User Test API Working"
            },
            status=status.HTTP_200_OK
        )
    
class EmployerJobsAPIView(ListAPIView):

    serializer_class = JobSerializer

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def get_queryset(self):

        recruiter = Recruiter.objects.get(
            user__email=self.request.user.email
        )

        return Job.objects.filter(
            recruiter=recruiter
        ).order_by("-created_at")    
    
from applications.models import Application
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class EmployerAnalyticsAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def get(self, request):

        recruiter = Recruiter.objects.get(
            user__email=request.user.email
        )

        jobs = Job.objects.filter(
            recruiter=recruiter
        )

        total_jobs = jobs.count()

        total_applications = Application.objects.filter(
            job__in=jobs
        ).count()

        shortlisted = Application.objects.filter(
            job__in=jobs,
            status="shortlisted"
        ).count()

        selected = Application.objects.filter(
            job__in=jobs,
            status="selected"
        ).count()

        rejected = Application.objects.filter(
            job__in=jobs,
            status="rejected"
        ).count()

        shortlist_ratio = 0
        if total_applications > 0:
            shortlist_ratio = round(
                (shortlisted / total_applications) * 100,
                2
            )

        return Response({
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "shortlisted": shortlisted,
            "selected": selected,
            "rejected": rejected,
            "shortlist_ratio": shortlist_ratio
        })


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .answer_service import evaluate_answer
from .serializers import AnswerEvaluationSerializer
from .logging_service import LoggingService
from .security import EncryptionService


class EvaluateAnswerAPIView(APIView):

    permission_classes = [IsAuthenticated]

    throttle_classes = [AIRateThrottle]

    def post(self, request, answer_id):

        evaluation = evaluate_answer(answer_id)

        logger = LoggingService()

        logger.log_ai_action(
            request.user,
            "Answer Evaluation",
            f"Answer ID {answer_id} evaluated"
        )

        serializer = AnswerEvaluationSerializer(evaluation)

        data = serializer.data

        security = EncryptionService()

        data["ai_feedback"] = security.decrypt(
            data["ai_feedback"]
        )

        return Response(data)



from rest_framework.views import APIView
from rest_framework.response import Response

from .answer_service import evaluate_answer
from .models import AnswerEvaluation
from .serializers import AnswerEvaluationSerializer
from .logging_service import LoggingService
from .security import EncryptionService

class EvaluationResultAPIView(APIView):

    def get(self, request, answer_id):

        evaluation = AnswerEvaluation.objects.get(
            answer_id=answer_id
        )

        serializer = AnswerEvaluationSerializer(evaluation)

        data = serializer.data

        security = EncryptionService()

        data["ai_feedback"] = security.decrypt(
            data["ai_feedback"]
        )

        return Response(data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from applications.models import Application
from .schedule_engine import SchedulingEngine
from .notifications import send_interview_notification
from .logging_service import LoggingService


class ScheduleInterviewAPIView(APIView):

    def post(self, request, application_id):

        try:
            application = Application.objects.get(id=application_id)

        except Application.DoesNotExist:

            logger = LoggingService()

            logger.log_error(
                "ApplicationNotFound",
                f"Application ID {application_id} not found",
                "ScheduleInterviewAPIView"
            )

            return Response(
                {
                    "success": False,
                    "message": "Application not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        engine = SchedulingEngine()

        schedule = engine.schedule_interview(application)

        if not schedule:

            return Response(
                {
                    "success": False,
                    "message": "No interview slots available"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        send_interview_notification(schedule)

        schedule.confirmation_sent = True
        schedule.save()

        logger = LoggingService()

        logger.log_admin_action(
            request.user,
            "Interview Scheduled",
            f"Application ID {application.id}"
        )

        return Response(
            {
                "success": True,
                "message": "Interview scheduled successfully",
                "application_id": application.id,
                "date": str(schedule.slot.date),
                "start_time": str(schedule.slot.start_time),
                "status": schedule.status
            },
            status=status.HTTP_200_OK
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.models import Application

from .report_service import CandidateReportService
from .report_serializer import CandidateReportSerializer
class CandidateReportAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRecruiter
    ]

    throttle_classes = [
    AIRateThrottle
    ]

    def get(self, request, application_id):

        application = Application.objects.get(
            id=application_id
        )

        report = CandidateReportService().generate(
            application
        )

        serializer = CandidateReportSerializer(
            report
        )

        return Response(serializer.data)    

from .analytics_service import AnalyticsService
from .permissions import IsRecruiter

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class AnalyticsDashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRecruiter
    ]

    throttle_classes = [
    AIRateThrottle
    ]

    def get(self, request):

        service = AnalyticsService()

        return Response(
            service.dashboard()
        )    