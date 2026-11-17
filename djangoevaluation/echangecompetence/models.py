from django.conf import settings
from django.db import models


class skill(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class belongSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill = models.ForeignKey("skill", on_delete=models.CASCADE)


class activity(models.Model):
    name = models.CharField(max_length=200)
    skill = models.ForeignKey("skill", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class plannedActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey("activity", on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
