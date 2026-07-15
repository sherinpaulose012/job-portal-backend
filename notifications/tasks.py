from .email_service import send_email


def send_email_async(to_email, subject, message):
    """
    Placeholder for asynchronous email sending.
    In production this can be replaced with Celery/RQ.
    """
    send_email(
        to_email=to_email,
        subject=subject,
        message=message
    )