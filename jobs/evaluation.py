KEYWORDS = {
    "Python",
    "Django",
    "SQL",
    "REST",
    "API",
    "React",
}


class AnswerScoringEngine:

    def evaluate(self, answer):

        text = answer.lower()

        matched = 0

        for keyword in KEYWORDS:

            if keyword.lower() in text:
                matched += 1

        keyword_score = matched * 10

        relevance = min(len(text) / 4, 100)

        completeness = 100 if len(text) > 80 else 60

        confidence = 90 if len(text) > 40 else 60

        final = (
            relevance * 0.30
            + completeness * 0.30
            + keyword_score * 0.20
            + confidence * 0.20
        )

        return {
            "relevance": round(relevance, 2),
            "completeness": round(completeness, 2),
            "keyword_score": round(keyword_score, 2),
            "confidence": confidence,
            "final_score": round(final, 2),
            "feedback": "Good technical answer."
        }