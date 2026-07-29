from rest_framework.views import APIView
from rest_framework.response import Response

from .reminder_tasks import send_interview_reminders


class SendReminderAPIView(APIView):

    def post(self, request):

        send_interview_reminders.delay()

        return Response({
            "success": True,
            "message": "Interview reminder scan started."
        })