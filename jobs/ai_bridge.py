from .llm_service import LLMService
from .voice_service import VoiceService
import time
from .security import check_rate_limit


class AIBridge:

    def __init__(self):
        self.llm = LLMService()
        self.voice = VoiceService()

    def start_interview(self, job_title):

        retries = 3
        check_rate_limit()

        for attempt in range(retries):

            try:

                print("=" * 50)
                print(f"Attempt {attempt + 1}")

                self.voice.select_voice()

                questions = self.llm.generate_questions(job_title)

                responses = []

                for question in questions:

                    self.voice.text_to_speech(question)

                    answer = self.voice.speech_to_text()

                    responses.append(
                        {
                            "question": question,
                            "answer": answer
                        }
                    )

                print("AI Interview Completed")

                return responses

            except Exception as e:

                print(f"Error : {e}")

                if attempt < retries - 1:
                    print("Retrying...")
                    time.sleep(2)

        print("Interview Failed")

        return []