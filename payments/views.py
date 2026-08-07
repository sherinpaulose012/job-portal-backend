from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import PaymentService
from rest_framework.permissions import AllowAny

class CreateOrderAPIView(APIView):

    def post(self, request):
        amount = request.data.get("amount", 0)

        order = PaymentService.create_order(amount)

        return Response(order, status=status.HTTP_201_CREATED)


class VerifyPaymentAPIView(APIView):

    def post(self, request):
        payment_id = request.data.get("payment_id")
        signature = request.data.get("signature")

        verified = PaymentService.verify_payment(
            payment_id,
            signature
        )

        return Response({
            "verified": verified
        })


class CapturePaymentAPIView(APIView):

    def post(self, request):
        payment_id = request.data.get("payment_id")

        result = PaymentService.capture_payment(payment_id)

        return Response(result)


class PaymentWebhookAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        event = request.data.get("event")

        if event == "payment.success":
            return Response({
                "message": "Payment Success Webhook Received"
            })

        elif event == "payment.failed":
            return Response({
                "message": "Payment Failed Webhook Received"
            })

        elif event == "refund.processed":
            return Response({
                "message": "Refund Webhook Received"
            })

        return Response({
            "message": "Unknown Event"
        }, status=400)    