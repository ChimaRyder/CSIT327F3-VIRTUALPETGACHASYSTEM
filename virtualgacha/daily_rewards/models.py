from django.db import models
from django.contrib.auth.models import User
from inventory.models import Pet
import datetime

class Reward(models.Model):
    date = models.DateField(default=datetime.date.today,unique=True)  # Date of the reward
    credit_reward = models.IntegerField(default=100)  # Reward details
    pet_reward = models.ForeignKey(Pet, on_delete=models.CASCADE,  null=True, blank=True)  # Reward details

    def __str__(self):
        return f"{self.date}"
    
class UserReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    claimed = models.BooleanField(default=False)
    claim_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.reward}"