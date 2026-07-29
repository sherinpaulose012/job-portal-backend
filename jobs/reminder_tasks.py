from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from .reminder_engine import ReminderEngine
from .models import ReminderLog


@shared_task(bind=True, max_retries=3)
def send_interview_reminders(self):

    engine = ReminderEngine()

    reminders = engine.get_pending_reminders()

    for schedule, reminder_type in reminders:

        try:

            candidate = schedule.application.candidate

            send_mail(
                subject="Interview Reminder",
                message=(
                    f"Dear {candidate.email},\n\n"
                    f"This is your {reminder_type} reminder.\n"
                    f"Your interview is scheduled on "
                    f"{schedule.slot.date} at "
                    f"{schedule.slot.start_time}.\n\n"
                    f"Please be available for your interview.\n\n"
                    f"Regards,\n"
                    f"AI Recruitment Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[candidate.email],
                fail_silently=False,
            )

            ReminderLog.objects.create(
                schedule=schedule,
                reminder_type=reminder_type,
                status="SENT"
            )

            print(f"Reminder sent to {candidate.email}")

        except Exception as exc:

            ReminderLog.objects.create(
                schedule=schedule,
                reminder_type=reminder_type,
                status="FAILED",
                error_message=str(exc)
            )

            raise self.retry(exc=exc, countdown=60)

    return "Reminder scan completed"