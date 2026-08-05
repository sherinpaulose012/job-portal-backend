from .models import (
    AuditTrail,
    ErrorLog,
    SecurityLog,
)


class LoggingService:

    def log_user_action(
        self,
        user,
        action,
        details=""
    ):

        AuditTrail.objects.create(
            user=user,
            action_type="USER",
            action=action,
            details=details
        )

    def log_admin_action(
        self,
        user,
        action,
        details=""
    ):

        AuditTrail.objects.create(
            user=user,
            action_type="ADMIN",
            action=action,
            details=details
        )

    def log_ai_action(
        self,
        user,
        action,
        details=""
    ):

        AuditTrail.objects.create(
            user=user,
            action_type="AI",
            action=action,
            details=details
        )

    def log_error(
        self,
        error_type,
        message,
        source
    ):

        ErrorLog.objects.create(
            error_type=error_type,
            message=message,
            source=source
        )

    def log_security(
        self,
        ip_address,
        event,
        user=None
    ):

        SecurityLog.objects.create(
            ip_address=ip_address,
            event=event,
            user=user
        )