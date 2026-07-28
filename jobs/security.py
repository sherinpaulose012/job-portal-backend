import time

LAST_CALL = 0


def check_rate_limit():

    global LAST_CALL

    current = time.time()

    if current - LAST_CALL < 5:
        raise Exception("Rate Limit Exceeded")

    LAST_CALL = current