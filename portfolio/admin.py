from django.contrib import admin
from .models import (
    Skill,
    Project,
    Profile,
    Experience,
    Education,
    ContactMessage
)

admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Profile)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(ContactMessage)