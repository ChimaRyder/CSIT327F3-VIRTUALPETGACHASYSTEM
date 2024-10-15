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
        pets.sort(key=lambda p: p.rarity)

        paginator = Paginator(pets, items_per_page)

        page = request.GET.get('page', 1)

        pets = paginator.get_page(page)

        return render(request, "inventory/inventory_list.html", {'inventory': inventory, 'pets': pets})

    return render(request, "inventory/inventory_list.html", {})


# pet view in inventory
def pet_view(request):
    pet_id = request.GET.get('pet_id')
    pet = Pet.objects.get(id=pet_id)

    return render(request, "pets/pet_view.html", {'pet': pet})


# send to an adventure (collect credits?)
def send_adventure(request):
    pass