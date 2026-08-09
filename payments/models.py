from django.db import models
from django.conf import settings
import uuid


class SubscriptionPlan(models.Model):

    PLAN_CHOICES = [
        ("FREE", "Free"),
        ("PRO", "Pro"),
        ("ENTERPRISE", "Enterprise"),
    ]

    name = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        unique=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    duration_days = models.IntegerField()

    description = models.TextField()

    job_post_limit = models.IntegerField(
        default=3
    )

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

    start_date = models.DateField(
        auto_now_add=True
    )

    end_date = models.DateField()

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"


class PaymentTransaction(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="payment_transactions"
    )

    subscription = models.ForeignKey(
        UserSubscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    payment_method = models.CharField(
        max_length=50,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.transaction_id} - "
            f"{self.user} - "
            f"{self.amount}"
        )


class BillingHistory(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    payment = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.CASCADE,
        related_name="billing_records"
    )

    invoice_number = models.CharField(
        max_length=100
    )

    billing_date = models.DateField(
        auto_now_add=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return (
            f"{self.invoice_number} - "
            f"{self.user.email}"
        )

class RefundLog(models.Model):

    payment = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.CASCADE,
        related_name="refund_logs"
    )

    refunded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    refund_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    reason = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"Refund - "
            f"{self.payment.transaction_id} - "
            f"{self.refund_amount}"
        )    

class FinancialAuditLog(models.Model):

    ACTION_CHOICES = [
        ("PAYMENT_SUCCESS", "Payment Success"),
        ("PAYMENT_FAILED", "Payment Failed"),
        ("REFUND", "Refund"),
        ("SUSPICIOUS", "Suspicious Transaction"),
    ]

    payment = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="financial_audit_logs"
    )

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.action} - {self.created_at}"    