class InterviewFlowManager:

    def __init__(self, questions):

        self.questions = questions
        self.current = 0

    def has_next(self):

        return self.current < len(self.questions)

    def next_question(self):

        question = self.questions[self.current]

        self.current += 1

        return question

class InterviewFlowManager:

    def __init__(self, questions):

        self.questions = questions
        self.current = 0

    def has_next(self):

        return self.current < len(self.questions)

    def next_question(self):

        question = self.questions[self.current]

        self.current += 1

        return question

    def follow_up(self, answer):

        if "yes" in answer.lower():

            return "Can you explain further?"

        if "django" in answer.lower():

            return "Explain Django Middleware."

        if "python" in answer.lower():

            return "Explain Python Generators."

        return None
        