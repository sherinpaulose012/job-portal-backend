from django.urls import path

from .views import (
    JobListAPIView,
    JobCreateAPIView,
    JobUpdateAPIView,
    UserTestAPIView,
    FeaturedJobAPIView,
    LatestJobAPIView,
    EmployerJobsAPIView,
    EmployerAnalyticsAPIView,

    # NEW
    EvaluateAnswerAPIView,
    EvaluationResultAPIView,
    ScheduleInterviewAPIView,
    CandidateReportAPIView,
    AnalyticsDashboardAPIView,
    PremiumCandidateRankingAPIView,
)

from .reminder_views import SendReminderAPIView

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

    # -----------------------------
    # AI Answer Evaluation APIs
    # -----------------------------

    path(
        "ai/evaluate/<int:answer_id>/",
        EvaluateAnswerAPIView.as_view(),
        name="evaluate-answer"
    ),

    path(
        "ai/evaluation/<int:answer_id>/",
        EvaluationResultAPIView.as_view(),
        name="evaluation-result"
    ),

    path(
    "interview/schedule/<int:application_id>/",
    ScheduleInterviewAPIView.as_view(),
    name="schedule-interview"
),

    path(
    "interview/reminders/",
    SendReminderAPIView.as_view(),
    name="send-reminders"
),

path(
    "ai/report/<int:application_id>/",
    CandidateReportAPIView.as_view(),
    name="candidate-report"
),

path(
    "analytics/dashboard/",
    AnalyticsDashboardAPIView.as_view(),
    name="analytics-dashboard"
),

path(
    "premium/candidate-ranking/<int:job_id>/",
    PremiumCandidateRankingAPIView.as_view(),
),

]