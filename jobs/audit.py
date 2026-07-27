from .models import CallLog


def create_call_log(session, event, triggered_by):
    """
    Creates an audit log for every AI interview event.
    """

    return CallLog.objects.create(
        session=session,
        event=event,
        triggered_by=triggered_by
    )