from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class AuthenticationTest(APITestCase):

    def test_login_required(self):

        response = self.client.get(
            "/applications/history/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


from accounts.models import User
from jobs.models import Job
from applications.models import Application

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from jobs.models import Recruiter

class JobApplicationFlowTest(APITestCase):

    def setUp(self):

# Employer User
        self.employer = User.objects.create_user(
        email="emp@test.com",
        password="test123",
        role="EMPLOYER"
)

# Recruiter Profile
        self.recruiter = Recruiter.objects.create(
        user=self.employer
        )

        # Candidate
        self.candidate = User.objects.create_user(
            email="can@test.com",
            password="test123",
            role="CANDIDATE"
        )

        # Job
        self.job = Job.objects.create(
        recruiter=self.recruiter,
        title="Python Developer",
        description="Backend Developer",
        skills="Python,Django",
        experience=1,
        salary_min=30000,
        salary_max=50000,
        location="Kochi",
        job_type="FULL_TIME",
        status=True
)

        # JWT Token
        refresh = RefreshToken.for_user(self.candidate)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

    def test_candidate_can_apply(self):

        response = self.client.post(
            f"/applications/jobs/{self.job.id}/apply/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Application.objects.filter(
                candidate=self.candidate,
                job=self.job
            ).exists()
        )        