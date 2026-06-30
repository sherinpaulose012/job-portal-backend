from django.db import models
from django.conf import settings


def resume_upload_path(instance, filename):
    extension = filename.split(".")[-1]
    return f"resumes/candidate_{instance.user.id}.{extension}"


class CandidateProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidate_profile"
    )

    skills = models.TextField()
    education = models.TextField()
    experience = models.IntegerField()
    expected_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    resume = models.FileField(
        upload_to=resume_upload_path,
        blank=True,
        null=True
    )

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class EmployerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employer_profile"
    )

    
    company_name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    company_size = models.IntegerField()
    verification = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name