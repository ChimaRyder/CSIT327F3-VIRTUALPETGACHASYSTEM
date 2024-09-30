from django.db import models
from django.contrib.auth.models import User # Can be changed later if a custom User model is made, only foreign key is required

# Create your models here.
class Inventory(models.Model):
    total_pets = models.IntegerField(default=0)  # Needs pet keys to change to a derived field
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Pets(models.Model):
    class Rarity(models.IntegerChoices):
        COMMON = 0
        UNCOMMON = 1
        RARE = 2
        MYTHICAL = 3
        LEGENDARY = 4

    pet_species = models.CharField(max_length=50)
    rarity = models.IntegerField(choices=Rarity.choices)
    is_busy = models.BooleanField(default=False)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)