from django.urls import path
from .views import (
    CreateOrderAPIView,
    VerifyPaymentAPIView,
    CapturePaymentAPIView,
    PaymentWebhookAPIView,
    SubscriptionStatusAPIView,
    AdminTransactionListAPIView,
    AdminRevenueAPIView,
    AdminRefundAPIView,
    AdminFinancialAuditLogAPIView,
)

urlpatterns = [
    path("create-order/", CreateOrderAPIView.as_view(), name="create-order"),
    path("verify-payment/", VerifyPaymentAPIView.as_view(), name="verify-payment"),
    path("capture-payment/", CapturePaymentAPIView.as_view(), name="capture-payment"),
    path("webhook/",PaymentWebhookAPIView.as_view(),name="payment-webhook"),
    path("subscription/status/",SubscriptionStatusAPIView.as_view(),name="subscription-status"),
    path("admin/transactions/",AdminTransactionListAPIView.as_view(),name="admin-transactions"),
    path("admin/revenue/",AdminRevenueAPIView.as_view(),name="admin-revenue"),
    path("admin/refund/<int:transaction_id>/", AdminRefundAPIView.as_view(), name="admin-refund"),
    path("admin/audit-logs/", AdminFinancialAuditLogAPIView.as_view(), name="admin-financial-audit-logs"),
]