from applications.models import Application


class PremiumRecruiterReportService:

    @staticmethod
    def candidate_ranking(job_id):

        applications = (
            Application.objects
            .filter(job_id=job_id)
            .select_related("candidate")
            .prefetch_related(
                "ai_sessions__questions__answers__evaluation"
            )
        )

        candidates = []

        for application in applications:

            # -------------------------
            # ATS SCORE
            # -------------------------

            ats_score = 0

            if hasattr(application, "atsscore"):
                ats_score = application.atsscore.score

            # -------------------------
            # AI SCORE
            # -------------------------

            ai_scores = []

            for session in application.ai_sessions.all():

                for question in session.questions.all():

                    for answer in question.answers.all():

                        if hasattr(answer, "evaluation"):
                            ai_scores.append(
                                answer.evaluation.final_score
                            )

            if ai_scores:
                ai_score = sum(ai_scores) / len(ai_scores)
            else:
                ai_score = 0

            # -------------------------
            # FINAL SCORE
            # -------------------------

            final_score = (
                (ats_score * 0.5)
                +
                (ai_score * 0.5)
            )

            candidates.append({
                "application_id": application.id,
                "candidate": application.candidate.email,
                "ats_score": round(ats_score, 2),
                "ai_score": round(ai_score, 2),
                "final_score": round(final_score, 2),
                "status": application.status
            })

        # Highest score first

        candidates.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        # Add ranking

        for index, candidate in enumerate(
            candidates,
            start=1
        ):

            candidate["rank"] = index

        return candidates