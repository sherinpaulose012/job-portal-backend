from rest_framework import serializers


class CandidateReportSerializer(serializers.Serializer):

    candidate = serializers.EmailField()

    job = serializers.CharField()

    ats_score = serializers.FloatField()

    ai_score = serializers.FloatField()

    strengths = serializers.ListField()

    risks = serializers.ListField()

    overall = serializers.CharField()