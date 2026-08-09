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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import UserSubscription
from jobs.models import Job, Recruiter


class SubscriptionStatusAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        subscription = (
            UserSubscription.objects
            .filter(
                user=request.user,
                is_active=True,
                end_date__gte=timezone.now().date()
            )
            .select_related("plan")
            .order_by("-end_date")
            .first()
        )

        if not subscription:
            return Response({
                "active": False,
                "message": "No active subscription."
            })

        job_count = 0

        try:
            recruiter = Recruiter.objects.get(
                user=request.user
            )

            job_count = Job.objects.filter(
                recruiter=recruiter,
                status=True
            ).count()

        except Recruiter.DoesNotExist:
            pass

        return Response({
            "active": True,
            "plan": subscription.plan.name,
            "start_date": subscription.start_date,
            "end_date": subscription.end_date,
            "job_post_limit": subscription.plan.job_post_limit,
            "jobs_used": job_count,
            "jobs_remaining": max(
                subscription.plan.job_post_limit - job_count,
                0
            )
        })    

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import PaymentTransaction
from .serializers import PaymentTransactionSerializer

from accounts.permissions import IsAdmin


class AdminTransactionListAPIView(ListAPIView):

    serializer_class = PaymentTransactionSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):
        return PaymentTransaction.objects.select_related(
            "user",
            "plan"
        ).order_by("-created_at")

from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncMonth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import PaymentTransaction
from accounts.permissions import IsAdmin


class AdminRevenueAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        successful_payments = PaymentTransaction.objects.filter(
            status="SUCCESS"
        )

        total_revenue = (
            successful_payments.aggregate(
                total=Sum("amount")
            )["total"] or 0
        )

        daily_revenue = (
            successful_payments
            .annotate(
                date=TruncDate("created_at")
            )
            .values("date")
            .annotate(
                revenue=Sum("amount")
            )
            .order_by("-date")
        )

        monthly_revenue = (
            successful_payments
            .annotate(
                month=TruncMonth("created_at")
            )
            .values("month")
            .annotate(
                revenue=Sum("amount")
            )
            .order_by("-month")
        )

        plan_revenue = (
            successful_payments
            .values(
                "plan__name"
            )
            .annotate(
                revenue=Sum("amount")
            )
            .order_by("-revenue")
        )

        return Response({
            "total_revenue": total_revenue,
            "daily_revenue": daily_revenue,
            "monthly_revenue": monthly_revenue,
            "plan_wise_revenue": plan_revenue
        })

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import PaymentTransaction, RefundLog
from accounts.permissions import IsAdmin
from .models import PaymentTransaction, RefundLog, FinancialAuditLog

class AdminRefundAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def post(self, request, transaction_id):

        payment = get_object_or_404(
            PaymentTransaction,
            id=transaction_id
        )

        if payment.status != "SUCCESS":
            return Response(
                {
                    "success": False,
                    "message": "Only successful payments can be refunded."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        reason = request.data.get(
            "reason",
            "Refund processed by admin."
        )

        refund = RefundLog.objects.create(
            payment=payment,
            refunded_by=request.user,
            refund_amount=payment.amount,
            reason=reason
        )

        payment.status = "REFUNDED"
        payment.save(update_fields=["status"])

        FinancialAuditLog.objects.create(
        payment=payment,
        performed_by=request.user,
        action="REFUND",
        description=f"Payment of ₹{payment.amount} refunded by admin.")

        return Response(
            {
                "success": True,
                "message": "Payment refunded successfully.",
                "transaction_id": str(
                    payment.transaction_id
                ),
                "refund_amount": refund.refund_amount,
                "reason": refund.reason
            },
            status=status.HTTP_200_OK
        )    

from .models import FinancialAuditLog
from .serializers import FinancialAuditLogSerializer


class AdminFinancialAuditLogAPIView(ListAPIView):

    serializer_class = FinancialAuditLogSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get_queryset(self):
        return FinancialAuditLog.objects.select_related(
            "payment",
            "performed_by"
        ).order_by("-created_at")    