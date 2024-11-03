from enum import Enum
from django.db import models
from django.contrib.auth.models import User # Can be changed later if a custom User model is made, only foreign key is required
from django.utils import timezone


# Create your models here.

class Pet(models.Model):
    class Rarity(models.IntegerChoices):
        COMMON = 0, 'Common'
        UNCOMMON = 1, 'Uncommon'
        RARE = 2, 'Rare'
        MYTHICAL = 3, 'Mythical'
        LEGENDARY = 4, 'Legendary'

    pet_rate = models.FloatField(null=True, blank=True)
    pet_species = models.CharField(max_length=50)
    rarity = models.IntegerField(choices=Rarity.choices)
    pet_image = models.ImageField(upload_to='pets/', null=True, blank=True)

    def __str__(self):
        return f'{self.pet_species}'

class Inventory(models.Model):
    class BusyValue(models.IntegerChoices):
        NOT_BUSY = 0, 'Not Busy'
        BUSY = 1, 'Busy'
        ON_MARKET = 2, 'On Market'

    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE, default=None, null=True, blank=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_busy = models.IntegerField(choices=BusyValue.choices)
    date_acquired = models.DateTimeField(default=timezone.now)

    # def __str__(self):
    #     return f'{self.owner_id.username}-{self.pet_id}'