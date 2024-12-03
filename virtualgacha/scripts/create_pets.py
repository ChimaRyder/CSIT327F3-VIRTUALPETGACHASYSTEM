import os
from inventory.models import Pet
import random

def create_pets_from_folder(folder_name):
    base_path = './media/pets'
    folder_path = os.path.join(base_path, folder_name)

    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist.")
        print(f"Current working directory: {os.getcwd()}")
        return

    rarity_map = {
        'Common': Pet.Rarity.COMMON,
        'Uncommon': Pet.Rarity.UNCOMMON,
        'Rare': Pet.Rarity.RARE,
        'Mythical': Pet.Rarity.MYTHICAL,
        'Legendary': Pet.Rarity.LEGENDARY,
    }

    rate_map = {
        'Common': (100, 150),
        'Uncommon': (200, 300),
        'Rare': (400, 600),
        'Mythical': (800, 1000),
        'Legendary': (1900, 2000),
    }


    rarity = rarity_map.get(folder_name)
    rate = rate_map.get(folder_name)
    if rarity is None:
        print(f"Rarity {folder_name} is not recognized.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            pet_species = os.path.splitext(filename)[0]  # Use the filename without extension as the pet species
            pet_image = file_path.replace('./media', '')  # Remove the leading './' from the file path

            # Create the Pet object
            pet = Pet(
                pet_species=pet_species,
                rarity=rarity,
                pet_image=pet_image,
                pet_rate= random.uniform(rate[0], rate[1])
            )
            pet.save()
            print(f"Created pet: {pet_species} with rarity {folder_name}")

# Example usage


def run(*args):
    # create_pets_from_folder('Common')
    # create_pets_from_folder('Uncommon')
    # create_pets_from_folder('Rare')
    # create_pets_from_folder('Mythical')
    create_pets_from_folder('Legendary')