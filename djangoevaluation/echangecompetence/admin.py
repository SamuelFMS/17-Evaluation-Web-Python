from django.contrib import admin

from .models import Activity, BelongSkill, PlannedActivity, Skill


class SkillAdmin(admin.ModelAdmin):
    fields = ["name"]
    ordering = ["name"]
    search_fields = ["name"]


class BelongSkillAdmin(admin.ModelAdmin):
    fields = ["user", "skill"]
    ordering = ["user", "skill__name"]
    search_fields = ["user__username", "skill__name"]
    list_filter = ["user__username", "skill__name"]
    list_display = ["user__username", "skill__name"]


class ActivityAdmin(admin.ModelAdmin):
    fields = ["name", "skill"]
    list_display = ["name", "skill__name"]
    ordering = ["skill__name", "name"]
    search_fields = ["name", "skill__name"]
    list_filter = ["skill__name"]


class PlannedActivityAdmin(admin.ModelAdmin):
    fields = ["user", "activity", "description", "date", "reserved_by"]
    ordering = ["date", "user", "activity__name"]
    search_fields = ["user__username", "activity__name"]
    list_filter = ["user__username", "activity__name", "date"]
    list_display = ["user", "activity", "description", "date", "reserved_by"]


admin.site.register(Skill, SkillAdmin)
admin.site.register(BelongSkill, BelongSkillAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(PlannedActivity, PlannedActivityAdmin)
