from rest_framework.permissions import BasePermission
from django.utils import timezone
from datetime import timedelta

from .models import UserSubscription


class HasActiveSubscription(BasePermission):

    message = "Active subscription required."

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        subscription = UserSubscription.objects.filter(
            user=request.user
        ).order_by("-end_date").first()

        if not subscription:
            return False

        today = timezone.now().date()

        # Active subscription
        if subscription.is_active and subscription.end_date >= today:
            return True

        # Grace period: 3 days after expiry
        grace_period_end = subscription.end_date + timedelta(days=3)

        if today <= grace_period_end:
            return True

        return False

from django.utils import timezone
from .models import UserSubscription


def get_active_subscription(user):
    return UserSubscription.objects.filter(
        user=user,
        is_active=True,
        end_date__gte=timezone.now().date()
    ).select_related("plan").first()


def has_active_subscription(user):
    return get_active_subscription(user) is not None    