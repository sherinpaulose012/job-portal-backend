def determine_status(score):

    if score >= 80:
        return "shortlisted"

    elif score >= 50:
        return "under_review"

    return "rejected"


def auto_process(result):

    score = result["score"]

    return determine_status(score)


def is_eligible(score):

    return score >= 50