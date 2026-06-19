from rest_framework import serializers
from .models import Application
from rest_framework import serializers
from .models import ApplicationStatusLog


class ApplicationStatusLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatusLog
        fields = "__all__"

class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = [
            "candidate",
            "status",
            "applied_date",
        ]