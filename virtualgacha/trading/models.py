from django.db import models
from django.utils import timezone

from inventory.models import Inventory


# Create your models here.

class Trade(models.Model):
    class TradeStatus(models.TextChoices):
        available = 'available', 'Available'
        waiting = 'waiting', 'Waiting'
        success = 'success', 'Success'
        closed = 'closed', 'Closed'

    pet_to_trade = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='pet_to_trade')
    pet_to_offer = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='pet_to_offer', null=True, blank=True)
    pet_preferences = models.JSONField(default=list, blank=True)
    status = models.CharField(choices=TradeStatus.choices, default=TradeStatus.available, max_length=20)
    date_created = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField(null=True, blank=True)
