from django.core.management.base import BaseCommand

from applications.models import Application, ATSScore
from profiles.models import CandidateProfile
from candidate.ats import calculate_ats_score
from candidate.automation import auto_process


class Command(BaseCommand):
    help = "Process all pending applications"

    def handle(self, *args, **kwargs):

        applications = Application.objects.filter(status="applied")

        for application in applications:

            profile = CandidateProfile.objects.get(
                user=application.candidate
            )

            result = calculate_ats_score(
                profile.parsed_resume,
                application.job
            )

            status = auto_process(result)

            application.status = status
            application.save()

            ATSScore.objects.update_or_create(
                application=application,
                defaults={
                    "score": result["score"],
                    "matched_skills": result["matched_skills"]
                }
            )

            self.stdout.write(
                f"Processed Application {application.id}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Batch Processing Completed"
            )
        )