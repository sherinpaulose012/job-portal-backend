from jobs.eligibility import check_candidate_eligibility
from jobs.tasks import trigger_ai_interview


def process_ai_interview(application):
    """
    Checks eligibility and queues an AI interview.
    """

    eligible, message = check_candidate_eligibility(application)

    if not eligible:
        return {
            "status": "Rejected",
            "reason": message
        }

    # Update call status
    application.call_status = "QUEUED"
    application.save()

    # Trigger Celery task
    trigger_ai_interview.delay(application.id)

    return {
        "status": "Queued",
        "reason": "AI Interview Scheduled"
    }