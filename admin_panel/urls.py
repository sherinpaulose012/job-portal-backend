from django.urls import path
from .views import (
    ApproveEmployerAPIView,
    BlockUserAPIView,
    AdminJobListAPIView,
    DeleteJobAPIView,
    AdminJobStatusAPIView,
    DashboardAPIView,
    UserGrowthAPIView,
    JobActivityAPIView,
    RemoveSpamJobAPIView,
    FlagUserAPIView,
    AuditLogAPIView,
)


urlpatterns = [
    path(
        "employers/<int:id>/approve/",
        ApproveEmployerAPIView.as_view(),
        name="approve-employer",
    ),

    path(
        "users/<int:id>/block/",
        BlockUserAPIView.as_view(),
        name="block-user",
    ),

    path(
    "jobs/",
    AdminJobListAPIView.as_view(),
    name="admin-job-list",
),

    path(
    "jobs/<int:id>/",
    DeleteJobAPIView.as_view(),
    name="delete-job",
),

    path(
    "jobs/<int:id>/status/",
    AdminJobStatusAPIView.as_view(),
    name="admin-job-status",
),

    path(
    "dashboard/",
    DashboardAPIView.as_view(),
    name="admin-dashboard",
),

    path(
    "user-growth/",
    UserGrowthAPIView.as_view(),
    name="user-growth",
),

    path(
    "job-activity/",
    JobActivityAPIView.as_view(),
    name="job-activity",
),

    path(
    "jobs/<int:id>/spam/",
    RemoveSpamJobAPIView.as_view(),
    name="remove-spam-job",
),

    path(
    "users/<int:id>/flag/",
    FlagUserAPIView.as_view(),
    name="flag-user",
    ),

    path(
    "audit-logs/",
    AuditLogAPIView.as_view(),
    name="audit-logs",
),    
]