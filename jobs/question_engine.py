from .question_templates import (
    INTRODUCTION,
    EXPERIENCE,
    SKILLS,
    AVAILABILITY,
    SALARY,
)


class DynamicQuestionEngine:

    def generate_questions(self, job):

        questions = []

        # Introduction
        questions.extend(INTRODUCTION)

        # Experience
        questions.extend(EXPERIENCE)

        # Skills based on Job

        for skill in job.required_skills:

            if skill in SKILLS:
                questions.extend(SKILLS[skill])

        # Availability

        questions.extend(AVAILABILITY)

        # Salary

        questions.extend(SALARY)

        return questions