from .tasks import send_interview_confirmation_email


def send_interview_notification(schedule):

    application = schedule.application

    send_interview_confirmation_email.delay(
        application.candidate.email,
        application.job.title,
        schedule.slot.date,
        schedule.slot.start_time,
    )