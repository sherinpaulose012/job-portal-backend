from .evaluation import AnswerScoringEngine
from .models import AIAnswer, AnswerEvaluation


def evaluate_answer(answer_id):

    answer = AIAnswer.objects.get(id=answer_id)

    engine = AnswerScoringEngine()

    result = engine.evaluate(answer.answer)

    evaluation = AnswerEvaluation.objects.create(
        answer=answer,
        relevance_score=result["relevance"],
        completeness_score=result["completeness"],
        keyword_score=result["keyword_score"],
        confidence=result["confidence"],
        final_score=result["final_score"],
        ai_feedback=result["feedback"]
    )

    return evaluation