from django.db import models
from django.contrib.auth.models import User # Can be changed later if a custom User model is made, only foreign key is required

# Create your models here.
class Inventory(models.Model):
    total_pets = models.IntegerField(default=0)  # Needs pet keys to change to a derived field
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
