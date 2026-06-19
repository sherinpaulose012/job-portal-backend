from django.contrib import admin
from .models import User, Recruiter, Job

admin.site.register(User)
admin.site.register(Recruiter)
admin.site.register(Job)