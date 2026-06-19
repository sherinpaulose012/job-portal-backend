from django.urls import path
from .views import (
    SignupView,
    LoginView,
    ProfileView,
    EmployerDashboardView,
)

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("login/", LoginView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("employer-test/", EmployerDashboardView.as_view()),
]