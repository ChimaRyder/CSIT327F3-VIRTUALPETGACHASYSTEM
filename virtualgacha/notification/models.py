from random import choices

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Notification(models.Model):
    class Status(models.TextChoices):
        unread = "Unread"
        read = "Read"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notif_status = models.TextField(choices=Status.choices, default=Status.unread)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    claim_coins = models.IntegerField(default=0)


