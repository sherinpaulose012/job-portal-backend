from rest_framework import serializers
from employer.models import Employer


class EmployerApprovalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employer
        fields = [
            "id",
            "company_name",
            "is_approved",
        ]

from accounts.models import User


class UserBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "role",
            "is_active",
            "is_flagged",
            "flag_reason",
        ]    

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuditLog
        fields = "__all__"