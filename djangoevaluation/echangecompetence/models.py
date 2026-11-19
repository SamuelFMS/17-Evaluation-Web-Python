from django.conf import settings
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BelongSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill = models.ForeignKey("skill", on_delete=models.CASCADE)


class Activity(models.Model):
    name = models.CharField(max_length=200)
    skill = models.ForeignKey("skill", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PlannedActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey("activity", on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    reserved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reserved_by",
    )

    def __str__(self):
        return self.description


class HelpRequest(models.Model):
    date = models.DateField()
    planned_activity = models.ForeignKey("PlannedActivity", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
