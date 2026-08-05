from .evaluation import AnswerScoringEngine
from .models import AIAnswer, AnswerEvaluation
from .security import EncryptionService


def evaluate_answer(answer_id):

    answer = AIAnswer.objects.get(id=answer_id)

    engine = AnswerScoringEngine()

    result = engine.evaluate(answer.answer)

    security = EncryptionService()

    encrypted_feedback = security.encrypt(
        result["feedback"]
    )

    evaluation = AnswerEvaluation.objects.create(
        answer=answer,
        relevance_score=result["relevance"],
        completeness_score=result["completeness"],
        keyword_score=result["keyword_score"],
        confidence=result["confidence"],
        final_score=result["final_score"],
        ai_feedback=encrypted_feedback
    )

    return evaluation