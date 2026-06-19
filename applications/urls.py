from django.urls import path
from .views import (
    ApplyJobAPIView,
    ApplicationHistoryAPIView,
    JobApplicantsAPIView,
    UpdateApplicationStatusAPIView,
    ApplicationLogAPIView
)

urlpatterns = [

    path(
        "jobs/<int:job_id>/apply/",
        ApplyJobAPIView.as_view()
    ),

    path(
        "history/",
        ApplicationHistoryAPIView.as_view()
    ),

    path(
        "jobs/<int:job_id>/applicants/",
        JobApplicantsAPIView.as_view()
    ),

     path(
        "update/<int:pk>/",
        UpdateApplicationStatusAPIView.as_view()
    ),

     path(
        "<int:pk>/logs/", 
        ApplicationLogAPIView.as_view()
    ),
]