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