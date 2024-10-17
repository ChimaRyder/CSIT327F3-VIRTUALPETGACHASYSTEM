from django.core.paginator import Paginator
from django.shortcuts import render

from inventory.models import Inventory, Pet


# inventory list backend
def inventory_list(request):
    items_per_page = 10
    user = request.user

    if Inventory.objects.filter(owner_id = user.id):
        inventory = Inventory.objects.filter(owner_id=user.id)

        #find pets associated with inventory
        pets = [inventory.pet_id for inventory in inventory]

        rarity_filter = []
        if request.GET:
            if request.GET.get('q'):
                pets = [p for p in pets if p.pet_species.lower().startswith(request.GET.get('q').lower())]
            if request.GET.get('sort'):
                if request.GET.get('sort') == 'acquisition':
                    pass
                if request.GET.get('sort') == 'rarity':
                    pets.sort(key=lambda p: p.rarity)
            if request.GET.get('rarity'):
                rarity_filter = request.GET.getlist('rarity')
                rarity_enum = ['Common', 'Uncommon', 'Rare', 'Mythical', 'Legendary']
                rarity_filter = [rarity_enum.index(r) for r in rarity_filter]
                pets = [p for p in pets if p.rarity in rarity_filter]


        paginator = Paginator(pets, items_per_page)

        page = request.GET.get('page', 1)

        pets = paginator.get_page(page)

        return render(request, "inventory/inventory_list.html", {'inventory': inventory, 'pets': pets, 'rarity_selected' : rarity_filter})

    return render(request, "inventory/inventory_list.html", {})


# pet view in inventory
def pet_view(request):
    pet_id = request.GET.get('pet_id')
    pet = Pet.objects.get(id=pet_id)

    return render(request, "pets/pet_view.html", {'pet': pet})


# send to an adventure (collect credits?)
def send_adventure(request):
    pass