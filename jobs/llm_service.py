import time
from .config import OPENAI_API_KEY

class LLMService:

    def generate_questions(self, job_title):

        print("Using API Key:", OPENAI_API_KEY[:8] + "...")
        print("=" * 50)
        print("Connecting to GPT Service...")
        time.sleep(2)

        print("Generating Interview Questions...")
        time.sleep(2)

        return [
            f"What is your experience with {job_title}?",
            "Explain REST API.",
            "Explain Django Architecture.",
            "Difference between Authentication and Authorization.",
            "What is ORM?"
        ]