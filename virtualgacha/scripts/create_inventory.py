import os
import django
import random
from django.contrib.auth.models import User
from inventory.models import Pet, Inventory
from django.utils import timezone

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

def create_dummy_inventory(num_entries=50):
    users = list(User.objects.all())
    pets = list(Pet.objects.all())

    if not users or not pets:
        print("Not enough data to create inventory entries.")
        return

    for _ in range(num_entries):
        user = random.choice(users)
        pet = random.choice(pets)
        is_busy = random.choice([0, 1, 2])  # Randomly choose between NOT_BUSY, BUSY, and ON_MARKET

        inventory = Inventory.objects.create(
            pet_id=pet,
            owner_id=user,
            is_busy=is_busy,
            date_acquired=timezone.now()
        )
        print(f"Created inventory entry: {inventory}")

def run():
    create_dummy_inventory(300)