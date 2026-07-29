from .models import (
    AvailabilitySlot,
    InterviewSchedule,
)


class SchedulingEngine:

    def schedule_interview(self, application):

        # Find first available slot
        slot = (
            AvailabilitySlot.objects
            .filter(is_booked=False)
            .order_by("date", "start_time")
            .first()
        )

        if not slot:
            return None

        # Mark slot as booked
        slot.is_booked = True
        slot.save()

        # Create interview schedule
        schedule = InterviewSchedule.objects.create(
            application=application,
            slot=slot,
        )

        return schedule