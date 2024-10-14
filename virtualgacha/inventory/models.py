from enum import Enum
from django.db import models
from django.contrib.auth.models import User # Can be changed later if a custom User model is made, only foreign key is required

# Create your models here.

class Pet(models.Model):
    class Rarity(models.IntegerChoices):
        COMMON = 0
        UNCOMMON = 1
        RARE = 2
        MYTHICAL = 3
        LEGENDARY = 4

    pet_species = models.CharField(max_length=50)
    rarity = models.IntegerField(choices=Rarity.choices)
    is_busy = models.BooleanField(default=False)
    pet_image = models.ImageField(upload_to='pets/', null=True, blank=True)

class Inventory(models.Model):
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE, default=None, null=True, blank=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
