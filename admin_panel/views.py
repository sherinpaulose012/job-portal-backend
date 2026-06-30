from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from employer.models import Employer

from .permissions import IsAdmin
from .serializers import EmployerApprovalSerializer,UserBlockSerializer

from accounts.models import User

from jobs.models import Job
from jobs.serializers import JobSerializer
from rest_framework.generics import ListAPIView

from accounts.models import User
from employer.models import Employer
from jobs.models import Job

from django.db.models import Count
from django.db.models.functions import TruncMonth

from .models import AuditLog
from .serializers import AuditLogSerializer
from rest_framework.generics import ListAPIView


class ApproveEmployerAPIView(APIView):

    permission_classes = [IsAdmin]

    def patch(self, request, id):

        try:
            employer = Employer.objects.get(id=id)

        except Employer.DoesNotExist:

            return Response(
                {
                    "error": "Employer not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        employer.is_approved = True
        employer.save()

        AuditLog.objects.create(
            admin=request.user,
            action="Approved Employer",
            target=f"Employer ID {employer.id}"
        )

        serializer = EmployerApprovalSerializer(employer)

        return Response(
            {
                "message": "Employer approved successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    

class BlockUserAPIView(APIView):

    permission_classes = [IsAdmin]

    def patch(self, request, id):

        try:
            user = User.objects.get(id=id)

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        is_active = request.data.get("is_active")

        if is_active is None:

            return Response(
                {
                    "error": "is_active field is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_active = is_active
        user.save()

        AuditLog.objects.create(
            admin=request.user,
            action="Blocked User" if not user.is_active else "Unblocked User",
            target=f"User ID {user.id}"
        )

        serializer = UserBlockSerializer(user)

        return Response(
            {
                "message":
                    "User unblocked successfully"
                    if user.is_active
                    else "User blocked successfully",

                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class AdminJobListAPIView(ListAPIView):

    permission_classes = [IsAdmin]

    serializer_class = JobSerializer

    queryset = Job.objects.all().order_by("-created_at")

class DeleteJobAPIView(APIView):

    permission_classes = [IsAdmin]

    def delete(self, request, id):

        try:
            job = Job.objects.get(id=id)

        except Job.DoesNotExist:

            return Response(
                {
                    "error": "Job not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        job.delete()

        AuditLog.objects.create(
            admin=request.user,
            action="Deleted Job",
            target=f"Job ID {job.id}"
        )

        return Response(
            {
                "message": "Job deleted successfully"
            },
            status=status.HTTP_200_OK
        )
    
class AdminJobStatusAPIView(APIView):

    permission_classes = [IsAdmin]

    def patch(self, request, id):

        try:
            job = Job.objects.get(id=id)

        except Job.DoesNotExist:

            return Response(
                {
                    "error": "Job not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        status_value = request.data.get("status")

        if status_value is None:

            return Response(
                {
                    "error": "status field is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        job.status = status_value
        job.save()

        AuditLog.objects.create(
            admin=request.user,
            action="Deleted Job",
            target=f"Job ID {job.id}"
    )

        serializer = JobSerializer(job)

        return Response(
            {
                "message":
                    "Job activated successfully"
                    if job.status
                    else "Job deactivated successfully",

                "data": serializer.data
            }
        )    
    
class DashboardAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        data = {
            "total_users": User.objects.count(),

            "total_employers": Employer.objects.count(),

            "approved_employers": Employer.objects.filter(
                is_approved=True
            ).count(),

            "blocked_users": User.objects.filter(
                is_active=False
            ).count(),

            "total_jobs": Job.objects.count(),

            "active_jobs": Job.objects.filter(
                status=True
            ).count(),

            "inactive_jobs": Job.objects.filter(
                status=False
            ).count(),
        }

        return Response(data)
    
class UserGrowthAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        growth = (
            User.objects
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(users=Count("id"))
            .order_by("month")
        )

        data = []

        for item in growth:

            data.append(
                {
                    "month": item["month"].strftime("%Y-%m"),
                    "users": item["users"]
                }
            )

        return Response(data)  


class JobActivityAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        data = {
            "total_jobs": Job.objects.count(),

            "active_jobs": Job.objects.filter(
                status=True
            ).count(),

            "inactive_jobs": Job.objects.filter(
                status=False
            ).count(),

            "featured_jobs": Job.objects.filter(
                is_featured=True
            ).count(),
        }

        return Response(data)     

class RemoveSpamJobAPIView(APIView):

    permission_classes = [IsAdmin]

    def delete(self, request, id):

        try:
            job = Job.objects.get(id=id)

        except Job.DoesNotExist:

            return Response(
                {
                    "error": "Job not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        job.delete()

        return Response(
            {
                "message": "Spam job removed successfully"
            },
            status=status.HTTP_200_OK
        )    

class FlagUserAPIView(APIView):

    permission_classes = [IsAdmin]

    def patch(self, request, id):

        try:
            user = User.objects.get(id=id)

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        user.is_flagged = True
        user.flag_reason = request.data.get(
            "flag_reason",
            ""
        )

        user.save()
        AuditLog.objects.create(
            admin=request.user,
            action="Flagged User",
            target=f"User ID {user.id}"
        )

        serializer = UserBlockSerializer(user)

        return Response(
            {
                "message": "User flagged successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class AuditLogAPIView(ListAPIView):

    permission_classes = [IsAdmin]

    serializer_class = AuditLogSerializer

    queryset = AuditLog.objects.all().order_by("-created_at")    