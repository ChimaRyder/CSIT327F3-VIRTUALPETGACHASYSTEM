import os
import django
import random
from django.contrib.auth.models import User
from inventory.models import Inventory
from marketplace.models import Sale, Purchase
from django.utils import timezone

def create_dummy_sales_and_purchases(num_sales=10):
    users = list(User.objects.all())
    inventories = list(Inventory.objects.all())

    if not users or not inventories:
        print("Not enough data to create sales and purchases.")
        return

    # Create dummy sales
    for _ in range(num_sales):
        inventory = random.choice(inventories)
        cost = round(random.uniform(10, 1000), 2)  # Random cost between 10 and 1000
        inventory.is_busy = 2
        inventory.save()
        sale = Sale.objects.create(
            inventory=inventory,
            cost=cost,
            date_created=timezone.now(),
            is_active=random.choice([True, False])
        )
        print(f"Created sale: {sale}")

def run():
    create_dummy_sales_and_purchases(10)