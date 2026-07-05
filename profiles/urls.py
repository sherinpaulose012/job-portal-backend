from django.urls import path
from .views import (
    CandidateProfileAPIView,
    EmployerProfileAPIView,
    ResumeUploadView,
    ATSMatchAPIView,
)

urlpatterns = [
    path('candidate/', CandidateProfileAPIView.as_view()),
    path('candidate/<int:pk>/', CandidateProfileAPIView.as_view()),

    path('candidate/upload-resume/', ResumeUploadView.as_view()),

    path('employer/', EmployerProfileAPIView.as_view()),
    path('employer/<int:pk>/', EmployerProfileAPIView.as_view()),

    path(
    "candidate/ats/<int:job_id>/",
    ATSMatchAPIView.as_view(),
    name="ats-match",
),
]