import os
import django
import random
from django.utils import timezone
from inventory.models import Inventory
from trading.models import Trade

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

def create_dummy_trades(num_trades=10):
    inventories = list(Inventory.objects.all())

    if len(inventories) < 2:
        print("Not enough inventory items to create trades.")
        return

    for _ in range(num_trades):
        pet_to_trade = random.choice(inventories)
        pet_to_offer = random.choice(inventories)
        while pet_to_offer == pet_to_trade:
            pet_to_offer = random.choice(inventories)

        trade = Trade.objects.create(
            pet_to_trade=pet_to_trade,
            pet_to_offer=pet_to_offer,
            pet_preferences=[random.choice(inventories).id for _ in range(random.randint(1, 5))],
            status=random.choice([status for status, _ in Trade.TradeStatus.choices]),
            date_created=timezone.now(),
            date_completed=timezone.now() if random.choice([True, False]) else None
        )
        print(f"Created trade: {trade}")

def run():
    create_dummy_trades(10)