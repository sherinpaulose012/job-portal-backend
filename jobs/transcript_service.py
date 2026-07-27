from .models import Transcript


def save_transcript(session, conversation):
    """
    Stores the complete AI interview transcript.
    """

    transcript, created = Transcript.objects.get_or_create(
        session=session,
        defaults={
            "transcript": conversation
        }
    )

    if not created:
        transcript.transcript = conversation
        transcript.save()

    return transcript