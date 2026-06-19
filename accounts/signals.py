from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from candidate.models import Candidate
from employer.models import Employer


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:

        if instance.role == User.ROLE_CANDIDATE:
            Candidate.objects.create(
                user=instance
            )

        elif instance.role == User.ROLE_EMPLOYER:
            Employer.objects.create(
                user=instance
            )