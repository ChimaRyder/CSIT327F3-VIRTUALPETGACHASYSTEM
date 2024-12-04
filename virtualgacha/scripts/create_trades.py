import os
import django
import random
from django.utils import timezone
from inventory.models import Inventory
from trading.models import Trade
from datetime import timedelta

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


def create_dummy_trades(num_trades=10):
    inventories = list(Inventory.objects.all())

    end_date = timezone.now()
    start_date = end_date - timedelta(days=365) 

    if len(inventories) < 2:
        print("Not enough inventory items to create trades.")
        return

    for _ in range(num_trades):
        pet_to_trade = random.choice(inventories)
        pet_to_offer = random.choice(inventories)
        while pet_to_offer == pet_to_trade:
            pet_to_offer = random.choice(inventories)

        date_created = random_date(start_date, end_date)

        trade = Trade.objects.create(
            pet_to_trade=pet_to_trade,
            pet_to_offer=pet_to_offer if random.choice([True, False]) else None,
            pet_preferences = [
                f"{pet.pet_id.get_rarity_display()}/{pet.pet_id.pet_species}"
                for pet in random.sample(inventories, random.randint(1, 4))
            ],
            date_created=date_created,
        )
        print(f"Created trade: {trade}")

def run():
    create_dummy_trades(10)