# candidate/urls.py

from django.urls import path
from .views import ResumeUploadView,ATSMatchAPIView

urlpatterns = [
    path(
        'upload-resume/',
        ResumeUploadView.as_view(),
        name='upload-resume'
    ),

    path(
        "ats/<int:job_id>/",
        ATSMatchAPIView.as_view(),
        name="ats-match",
    ),
]