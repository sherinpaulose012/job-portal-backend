from django.urls import path

from .views import (
    JobListAPIView,
    JobCreateAPIView,
    JobUpdateAPIView,
    UserTestAPIView,
    FeaturedJobAPIView,
    LatestJobAPIView,
    EmployerJobsAPIView,
    EmployerAnalyticsAPIView
)

urlpatterns = [
    path(
        "jobs/",
        JobListAPIView.as_view()
    ),

    path(
        "jobs/create/",
        JobCreateAPIView.as_view()
    ),

    path(
        "jobs/<int:id>/edit/",
        JobUpdateAPIView.as_view()
    ),

    path(
        "user-test/",
        UserTestAPIView.as_view()
    ),

    path(
    "jobs/<int:id>/status/",
    JobUpdateAPIView.as_view()
),

    path(
    "jobs/featured/",
    FeaturedJobAPIView.as_view()
),

path(
    "jobs/latest/",
    LatestJobAPIView.as_view()
),

path(
    "employer/jobs/",
    EmployerJobsAPIView.as_view()
),

path(
    "employer/analytics/",
    EmployerAnalyticsAPIView.as_view()
),
]