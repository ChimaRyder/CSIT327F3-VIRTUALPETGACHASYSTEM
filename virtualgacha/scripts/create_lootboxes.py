import random
from inventory.models import Pet
from lootbox_market.models import Lootbox, LootboxDropTable

def create_lootboxes():
    # Fetch pets by rarity
    legendaries = list(Pet.objects.filter(rarity=Pet.Rarity.LEGENDARY))
    mythicals = list(Pet.objects.filter(rarity=Pet.Rarity.MYTHICAL))
    rares = list(Pet.objects.filter(rarity=Pet.Rarity.RARE))
    uncommons = list(Pet.objects.filter(rarity=Pet.Rarity.UNCOMMON))
    commons = list(Pet.objects.filter(rarity=Pet.Rarity.COMMON))

    # Ensure we have enough pets to create the lootboxes
    num_legendary = len(legendaries)
    num_mythical = len(mythicals)
    num_lootboxes = min(num_legendary, num_mythical // 2)

    if num_lootboxes == 0:
        print("Not enough pets to create lootboxes.")
        return

    for i in range(num_lootboxes):
        # Create a new lootbox
        lootbox = Lootbox(
            lootbox_name=f"Lootbox {i + 1}",
            rate_cost=100,  # Example rate cost
            is_available=True
        )
        lootbox.save()

        # Add pets to the lootbox
        pets_to_add = []

        # Add 1 legendary
        pets_to_add.append(legendaries.pop())

        # Add 2 mythicals
        selected_mythicals = random.sample(mythicals, 2)
        pets_to_add.extend(selected_mythicals)
        mythicals = [pet for pet in mythicals if pet not in selected_mythicals]

        # Add 3 rares
        pets_to_add.extend(random.choices(rares, k=3))

        # Add 4 uncommons
        pets_to_add.extend(random.choices(uncommons, k=4))

        # Add 10 commons
        pets_to_add.extend(random.choices(commons, k=10))

        # Create LootboxDropTable entries
        for pet in pets_to_add:
            drop_table_entry = LootboxDropTable(
                lootbox_id=lootbox,
                pet_id=pet
            )
            drop_table_entry.save()

        print(f"Created lootbox {lootbox.lootbox_name} with {len(pets_to_add)} pets.")

# Example usage


def run(*args):
    create_lootboxes()