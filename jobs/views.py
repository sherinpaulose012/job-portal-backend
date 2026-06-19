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