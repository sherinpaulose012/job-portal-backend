from datetime import timedelta
from django.utils import timezone

from .models import InterviewSchedule


class ReminderEngine:

    def get_pending_reminders(self):

        reminders = []

        now = timezone.now()

        upcoming = InterviewSchedule.objects.filter(
            status="SCHEDULED"
        )

        for schedule in upcoming:
            reminders.append((schedule, "24 Hour Reminder"))

        return reminders