from django.core.mail import send_mail
from django.conf import settings

from .models import EmailLog


def send_email(to_email, subject, message):

    try:

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False,
        )

        EmailLog.objects.create(
            recipient=to_email,
            subject=subject,
            status="SUCCESS"
        )

    except Exception as e:

        EmailLog.objects.create(
            recipient=to_email,
            subject=subject,
            status="FAILED",
            error_message=str(e)
        )

        raise