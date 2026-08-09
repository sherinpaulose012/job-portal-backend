from rest_framework import serializers

from .models import PaymentTransaction, BillingHistory,FinancialAuditLog


class PaymentTransactionSerializer(serializers.ModelSerializer):

    user_email = serializers.CharField(
        source="user.email",
        read_only=True
    )

    plan_name = serializers.CharField(
        source="plan.name",
        read_only=True
    )

    class Meta:
        model = PaymentTransaction
        fields = [
            "id",
            "transaction_id",
            "user_email",
            "plan_name",
            "amount",
            "status",
            "payment_method",
            "created_at",
        ]


class BillingHistorySerializer(serializers.ModelSerializer):

    user_email = serializers.CharField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = BillingHistory
        fields = [
            "id",
            "invoice_number",
            "user_email",
            "amount",
            "billing_date",
            "payment",
        ]

class FinancialAuditLogSerializer(serializers.ModelSerializer):

    admin_email = serializers.CharField(
        source="performed_by.email",
        read_only=True
    )

    transaction_id = serializers.CharField(
        source="payment.transaction_id",
        read_only=True
    )

    class Meta:
        model = FinancialAuditLog
        fields = [
            "id",
            "action",
            "description",
            "admin_email",
            "transaction_id",
            "created_at",
        ]        