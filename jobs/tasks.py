from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import time


@shared_task
def send_application_email(email, job_title):
    subject = "Application Submitted"
    message = (
        f"Your application for '{job_title}' "
        f"has been submitted successfully."
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    return "Email Sent"


@shared_task
def parse_resume(resume_id):
    print(f"Started parsing Resume ID: {resume_id}")

    time.sleep(5)

    print("Extracting text...")
    print("Finding Skills...")
    print("Finding Education...")
    print("Finding Experience...")

    return {
        "skills": ["Python", "Django", "SQL"],
        "education": "B.Tech",
        "experience": "Fresher",
    }


@shared_task
def trigger_ai_interview(application_id):

    print("=" * 50)
    print(f"Application ID : {application_id}")
    print("=" * 50)

    print("Call Status : QUEUED")
    time.sleep(2)

    print("Checking Candidate Eligibility...")
    time.sleep(2)

    print("Call Status : IN_PROGRESS")
    time.sleep(2)

    print("Generating AI Interview Questions...")
    time.sleep(2)

    print("Connecting Voice Interview Service...")
    time.sleep(2)

    print("Conducting AI Interview...")
    time.sleep(2)

    print("Calculating Interview Score...")
    time.sleep(2)

    print("Call Status : COMPLETED")
    print("=" * 50)

    return {
        "application_id": application_id,
        "status": "COMPLETED",
        "interview_score": 88,
        "questions_generated": True
    }