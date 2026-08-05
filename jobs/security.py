import time

LAST_CALL = 0


def check_rate_limit():

    global LAST_CALL

    current = time.time()

    if current - LAST_CALL < 5:
        raise Exception("Rate Limit Exceeded")

    LAST_CALL = current


import base64


class EncryptionService:

    def encrypt(self, text):

        if not text:
            return ""

        return base64.b64encode(
            text.encode()
        ).decode()

    def decrypt(self, text):

        if not text:
            return ""

        return base64.b64decode(
            text.encode()
        ).decode()    