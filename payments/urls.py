from django.urls import path
from .views import (
    CreateOrderAPIView,
    VerifyPaymentAPIView,
    CapturePaymentAPIView,
    PaymentWebhookAPIView,
)

urlpatterns = [
    path("create-order/", CreateOrderAPIView.as_view(), name="create-order"),
    path("verify-payment/", VerifyPaymentAPIView.as_view(), name="verify-payment"),
    path("capture-payment/", CapturePaymentAPIView.as_view(), name="capture-payment"),
    path("webhook/",PaymentWebhookAPIView.as_view(),name="payment-webhook"),
]