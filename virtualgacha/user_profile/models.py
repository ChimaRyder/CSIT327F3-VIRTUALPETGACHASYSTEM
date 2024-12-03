from django.db import models
from django.contrib.auth.models import User
from .achievements import achievements

# Create your models here.
class UserAchievements(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="achievements")
    achievement_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    date_earned = models.DateTimeField(auto_now_add=True)