from applications.models import Application
from .models import AnswerEvaluation


class CandidateReportService:

    def generate(self, application):

        ats_score = 85.0   # Placeholder for now

        evaluations = AnswerEvaluation.objects.filter(
    answer__question__session__application=application
)

        ai_score = 0

        if evaluations.exists():
            ai_score = sum(
                e.final_score for e in evaluations
            ) / evaluations.count()

        strengths = []
        risks = []

        if ai_score >= 80:
            strengths.append("Strong interview performance")
        elif ai_score >= 60:
            strengths.append("Good technical knowledge")
        else:
            risks.append("Needs technical improvement")

        if ats_score >= 80:
            strengths.append("Excellent ATS match")
        else:
            risks.append("Low ATS score")

        return {
            "candidate": application.candidate.email,
            "job": application.job.title,
            "ats_score": ats_score,
            "ai_score": round(ai_score, 2),
            "strengths": strengths,
            "risks": risks,
            "overall": "Recommended" if ai_score >= 70 else "Review",
        }