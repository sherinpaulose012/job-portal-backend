import time


class VoiceService:

    def speech_to_text(self):

        print("Speech → Text")
        time.sleep(2)

        return "Candidate response"

    def text_to_speech(self, text):

        print(f"Speaking : {text}")
        time.sleep(2)

        return True

    def select_voice(self, language="English"):

        print(f"Voice Selected : {language}")

        return "Female Voice"