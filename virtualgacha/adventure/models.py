from django.db import models
from inventory.models import Pet
from django.contrib.auth.models import User

# Create your models here.

class Adventure(models.Model):
    adventure_id = models.AutoField(primary_key=True)
    is_finished = models.BooleanField(default=False)
    is_claimed = models.BooleanField(default=False)
    total_earnings = models.FloatField(default=0)
    date_started = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField(blank=True, null=True)


class AdventurePet(models.Model):
    adventure_pet_id = models.AutoField(primary_key=True)
    adventure_id = models.ForeignKey(Adventure, on_delete=models.CASCADE)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)
    rate_multiplier = models.FloatField()
    rate_on_finish = models.FloatField()

class AdventureUser(models.Model):
    adventure_user_id = models.AutoField(primary_key=True)
    adventure_id = models.ForeignKey(Adventure, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    