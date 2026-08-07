from django.db import models
from django.conf import settings


class SubscriptionPlan(models.Model):

    PLAN_CHOICES = [
        ("FREE", "Free"),
        ("PRO", "Pro"),
        ("ENTERPRISE", "Enterprise"),
    ]

    name = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    duration_days = models.IntegerField()

    description = models.TextField()

    def __str__(self):
        return self.name


class UserSubscription(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE
    )

    start_date = models.DateField(auto_now_add=True)

    end_date = models.DateField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"


class PaymentTransaction(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    subscription = models.ForeignKey(
        UserSubscription,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_id = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)


class BillingHistory(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    payment = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.CASCADE
    )

    invoice_number = models.CharField(max_length=100)

    billing_date = models.DateField(auto_now_add=True)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )