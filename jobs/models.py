from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name


class Job(models.Model):

    JOB_TYPES = [
        ("FULL_TIME", "Full Time"),
        ("PART_TIME", "Part Time"),
        ("REMOTE", "Remote"),
    ]

    recruiter = models.ForeignKey(
        Recruiter,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    title = models.CharField(
        max_length=100
    )

    description = models.TextField()

    skills = models.TextField()

    experience = models.IntegerField()

    salary_min = models.IntegerField()

    salary_max = models.IntegerField()

    location = models.CharField(
        max_length=100
    )

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPES
    )

    status = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    is_featured = models.BooleanField(
        default=False
    )
    def __str__(self):
        return self.title

class Application(models.Model):

    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("shortlisted", "Shortlisted"),
        ("interview", "Interview Scheduled"),
        ("rejected", "Rejected"),
        ("selected", "Selected"),
    ]

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="applied"
    )

from django.db import models
from applications.models import Application
from accounts.models import User
import uuid


class AIInterviewSession(models.Model):

    STATUS_CHOICES = [
        ("QUEUED", "Queued"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="ai_sessions"
    )

    session_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    ended_at = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="QUEUED"
    )

    def __str__(self):
        return str(self.session_id)


class AIQuestion(models.Model):

    session = models.ForeignKey(
        AIInterviewSession,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question = models.TextField()

    order = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Q{self.order}: {self.question[:50]}"


class AIAnswer(models.Model):

    question = models.ForeignKey(
        AIQuestion,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    answer = models.TextField()

    score = models.FloatField(
        default=0.0
    )

    answered_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.answer[:50]


class Transcript(models.Model):

    session = models.OneToOneField(
        AIInterviewSession,
        on_delete=models.CASCADE,
        related_name="transcript"
    )

    transcript = models.JSONField(
        default=list,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Transcript - {self.session.session_id}"


class CallLog(models.Model):

    EVENT_CHOICES = [
        ("QUEUED", "Call Queued"),
        ("STARTED", "Call Started"),
        ("QUESTION_GENERATED", "Questions Generated"),
        ("IN_PROGRESS", "Interview In Progress"),
        ("COMPLETED", "Interview Completed"),
        ("FAILED", "Interview Failed"),
    ]

    session = models.ForeignKey(
        AIInterviewSession,
        on_delete=models.CASCADE,
        related_name="logs"
    )

    event = models.CharField(
        max_length=50,
        choices=EVENT_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    triggered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.session.session_id} - {self.event}"    