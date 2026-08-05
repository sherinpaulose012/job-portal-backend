from rest_framework.permissions import BasePermission

from .logging_service import LoggingService


class IsEmployer(BasePermission):

    def has_permission(self, request, view):

        if (
            request.user.is_authenticated
            and request.user.role == "EMPLOYER"
        ):
            return True

        logger = LoggingService()

        logger.log_security(
            request.META.get("REMOTE_ADDR"),
            "Unauthorized Employer Access",
            request.user if request.user.is_authenticated else None
        )

        return False


class IsRecruiter(BasePermission):

    def has_permission(self, request, view):

        if (
            request.user.is_authenticated
            and request.user.role == "EMPLOYER"
        ):
            return True

        logger = LoggingService()

        logger.log_security(
            request.META.get("REMOTE_ADDR"),
            "Unauthorized Recruiter Access",
            request.user if request.user.is_authenticated else None
        )

        return False