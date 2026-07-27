from applications.models import ATSScore


ATS_THRESHOLD = 70


def check_candidate_eligibility(application):
    """
    Checks whether a candidate is eligible for AI Interview.
    """

    try:
        ats = ATSScore.objects.get(application=application)
    except ATSScore.DoesNotExist:
        return False, "ATS score not available"

    # Rule 1
    if ats.score < ATS_THRESHOLD:
        return False, "ATS score below threshold"

    # Rule 2
    if application.status != "shortlisted":
        return False, "Candidate not shortlisted"

    # Rule 3
    # Rule 3
    if not application.job.status:

        return False, "Job is closed"

    return True, "Eligible"