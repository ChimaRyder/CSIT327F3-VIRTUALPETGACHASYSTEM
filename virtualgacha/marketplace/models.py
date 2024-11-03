from django.contrib.auth.models import User
from django.db import models

from inventory.models import Inventory
from django.utils import timezone


# Create your models here.
class Sale(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date_created}-{self.inventory}"

class Purchase(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_completed = models.DateTimeField(default=timezone.now)
