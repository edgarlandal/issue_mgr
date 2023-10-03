from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.


class Status(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    def _str_(self):
        return self.name


class Issue(models.Model):
    summary = models.CharField(max_length=512)
    description = models.TextField()
    reporter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    assignee = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="assignee",
        blank=True,
        null=True,
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.summary[:256]

    def get_absolute_url(self):
        return reverse("detail", args=[self.pk])
