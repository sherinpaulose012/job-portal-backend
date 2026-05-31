from django.urls import path
from .views import *

urlpatterns = [
    path('jobs/', JobListAPIView.as_view()),
    path('jobs/create/', JobCreateAPIView.as_view()),
    path('user-test/', UserTestAPIView.as_view()),
]