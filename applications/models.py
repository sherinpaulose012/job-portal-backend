from django.db import models
from accounts.models import User
from jobs.models import Job


class Application(models.Model):

    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("shortlisted", "Shortlisted"),
        ("interview", "Interview Scheduled"),
        ("selected", "Selected"),
        ("rejected", "Rejected"),
    ]

    CALL_STATUS = [
        ("QUEUED", "Queued"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications",
        db_index=True
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
        db_index=True
    )

    resume_snapshot = models.FileField(
        upload_to="applications/"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="applied",
        db_index=True
    )

    call_status = models.CharField(
    max_length=20,
    choices=CALL_STATUS,
    default="QUEUED"
)

    applied_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "candidate",
            "job"
        )

    def __str__(self):

        return (
            f"{self.candidate.email}"
            f" - "
            f"{self.job.title}"
        )
    
class ApplicationStatusLog(models.Model):

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="status_logs"
    )

    old_status = models.CharField(
        max_length=30
    )

    new_status = models.CharField(
        max_length=30
    )

    changed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    changed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.application.id}"
            f" | "
            f"{self.old_status}"
            f" → "
            f"{self.new_status}"
        )    
    
class SavedJob(models.Model):

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="saved_jobs"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="saved_by"
    )

    saved_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "candidate",
            "job"
        )    

class Notification(models.Model):

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.message        
    

class ATSScore(models.Model):

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE
    )

    score = models.FloatField(default=0)

    matched_skills = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application.id} - {self.score}"    
