import os
import django
import random
from django.contrib.auth.models import User
from inventory.models import Pet, Inventory
from lootbox_market.models import Lootbox,Pull, PullPet, LootboxDropTable



def create_random_pulls(num_pulls=10):
    users = list(User.objects.all())
    lootboxes = list(Lootbox.objects.all())
    pets = list(Pet.objects.all())


        

    if not users or not lootboxes or not pets:
        print("Not enough data to create pulls.")
        return

    for _ in range(num_pulls):
        user = random.choice(users)
        lootbox = random.choice(lootboxes)
        roll_info = random.choice([1,10])  # Random number of rolls between 1 and 10

        # Get the drop table for the selected lootbox
        drop_table = list(LootboxDropTable.objects.filter(lootbox_id=lootbox).select_related('pet_id'))
        
        # Create a new pull
        pull = Pull.objects.create(user_id=user, roll_info=roll_info, lootbox_id=lootbox)

        for _ in range(roll_info):
            pet = random.choice(drop_table).pet_id

            inventory = Inventory.objects.create(
                pet_id=pet,
                owner_id=user,
            )

            # Create a new PullPet entry
            PullPet.objects.create(pull_id=pull, pet_id=pet)

        print(f"Created pull {pull.pull_id} for user {user.username} with {roll_info} rolls.")

# Example usage
def run(*args):
    create_random_pulls(100)