from rest_framework import serializers
from .models import Resume
import magic


class ResumeUploadSerializer(serializers.Serializer):
    resume = serializers.FileField()

    def validate_resume(self, file):
        allowed_extensions = ['pdf', 'doc', 'docx']

        extension = file.name.split('.')[-1].lower()

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only PDF, DOC, and DOCX files are allowed."
            )

        if file.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "File size cannot exceed 5 MB."
            )

        # MIME type check (basic malware prevention)
        mime = magic.from_buffer(file.read(), mime=True)
        file.seek(0)

        allowed_mime = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]

        if mime not in allowed_mime:
            raise serializers.ValidationError(
                "Suspicious file detected"
            )

        return file

    def create(self, validated_data):
        request = self.context['request']
        candidate = request.user.candidate

        file = validated_data['resume']

        old_resumes = Resume.objects.filter(
            candidate=candidate,
            is_active=True
        )

        for old_resume in old_resumes:
            if old_resume.file:
                old_resume.file.delete(save=False)

        old_resumes.update(is_active=False)

        resume = Resume.objects.create(
            candidate=candidate,
            file=file,
            is_active=True
        )

        return resume