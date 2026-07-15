from django.db import models


class EmailLog(models.Model):

    recipient = models.EmailField()

    subject = models.CharField(max_length=200)

    status = models.CharField(max_length=20)

    error_message = models.TextField(
        blank=True,
        null=True
    )

    sent_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.recipient} - {self.status}"