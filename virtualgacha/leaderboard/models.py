from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)