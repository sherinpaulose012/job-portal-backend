from rest_framework import serializers
from .models import CandidateProfile, EmployerProfile


class CandidateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateProfile
        fields = '__all__'
        read_only_fields = ['user', 'is_deleted']

    def validate_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience cannot be negative")
        return value

    def validate_expected_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError("Salary must be greater than 0")
        return value

    def validate(self, data):
        request = self.context.get('request')

        # prevent duplicate profile
        if request and request.method == "POST":
            if CandidateProfile.objects.filter(user=request.user).exists():
                raise serializers.ValidationError("Candidate profile already exists")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
    
class EmployerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployerProfile
        fields = '__all__'
        read_only_fields = ['user', 'is_deleted']

    def validate_company_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Company name cannot be empty")
        return value

    def validate_company_size(self, value):
        if value <= 0:
            raise serializers.ValidationError("Company size must be greater than 0")
        return value

    def validate(self, data):
        request = self.context.get('request')

        if request and request.method == "POST":
            if EmployerProfile.objects.filter(user=request.user).exists():
                raise serializers.ValidationError("Employer profile already exists")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)   


class ResumeUploadSerializer(serializers.Serializer):

    resume = serializers.FileField()

    def validate_resume(self, file):

        allowed_extensions = ['pdf', 'doc', 'docx']

        extension = file.name.split('.')[-1].lower()

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only PDF, DOC and DOCX files are allowed."
            )

        if file.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "File size cannot exceed 5 MB."
            )
        
        return file     