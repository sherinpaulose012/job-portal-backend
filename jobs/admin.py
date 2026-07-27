from django.contrib import admin
from .models import (
    Job,
    AIInterviewSession,
    AIQuestion,
    AIAnswer,
    Transcript,
    CallLog,
)

admin.site.register(Job)
admin.site.register(AIInterviewSession)
admin.site.register(AIQuestion)
admin.site.register(AIAnswer)
admin.site.register(Transcript)
admin.site.register(CallLog)