from django.contrib import admin

from .models import skill, belongSkill, activity, plannedActivity

admin.site.register(skill)
admin.site.register(belongSkill)
admin.site.register(activity)
admin.site.register(plannedActivity)
