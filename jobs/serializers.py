from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = [
            "recruiter"
        ]

from rest_framework import serializers
from .models import AnswerEvaluation


class AnswerEvaluationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerEvaluation
        fields = "__all__"        