
import uuid
from datetime import datetime

from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator


class Candidate(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


def resume_upload_path(instance, filename):
    ext = filename.split('.')[-1]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:6]

    user_id = instance.candidate.user.id

    return f"resumes/user_{user_id}_{timestamp}_{unique_id}.{ext}"

class Resume(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    file = models.FileField(
        upload_to=resume_upload_path,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])]
    )

    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.user.email} Resume"