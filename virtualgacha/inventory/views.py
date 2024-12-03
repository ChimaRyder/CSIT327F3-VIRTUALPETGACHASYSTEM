from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from inventory.models import Inventory, Pet
from login_register.models import Profile
from marketplace.models import Sale
from notification.models import Notification


# inventory list backend
@login_required(login_url='login')
def inventory_list(request):
    items_per_page = 10
    user = request.user
    profile = Profile.objects.get(user=user)

    if Inventory.objects.filter(owner_id = user.id):
        inventory = Inventory.objects.select_related('pet_id').filter(owner_id=user.id)
        inventory = inventory.exclude(is_busy=1)

        rarity_filter = []
        if request.GET:
            if request.GET.get('sort'):
                if request.GET.get('sort') == 'acquisition':
                    inventory = inventory.order_by('date_acquired')
                if request.GET.get('sort') == 'rarity_ascending':
                    inventory = inventory.order_by('pet_id__rarity')
                if request.GET.get('sort') == 'rarity_descending':
                    inventory = inventory.order_by('pet_id__rarity').reverse()
                if request.GET.get('sort') == 'status':
                    inventory = inventory.order_by('is_busy').reverse()
            if request.GET.get('rarity'):
                rarity_filter = request.GET.getlist('rarity')
                rarity_enum = ['Common', 'Uncommon', 'Rare', 'Mythical', 'Legendary']
                rarity_filter = [rarity_enum.index(r) for r in rarity_filter]
                inventory = [inventory for inventory in inventory if inventory.pet_id.rarity in rarity_filter]
            if request.GET.get('q'):
                inventory = [inventory for inventory in inventory if inventory.pet_id.pet_species.lower().startswith(request.GET.get('q').lower())]

        paginator = Paginator(inventory, items_per_page)

        page = request.GET.get('page', 1)

        inventory = paginator.get_page(page)

        return render(request, "inventory/inventory_list.html", {'inventory': inventory, 'rarity_selected' : rarity_filter, 'profile': profile})

    return render(request, "inventory/inventory_list.html", {'profile': profile})


# pet view in inventory
def pet_view(request):
    pet_id = request.GET.get('pet_id')
    pet = Pet.objects.get(id=pet_id)

    return render(request, "pets/pet_view.html", {'pet': pet})


# send to an adventure (collect credits?)
def send_adventure(request):
    pass

def sell_pet(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        if request.POST.get('edit'):
            sale = Sale.objects.get(id=request.POST.get('sale'))
            sale.cost = request.POST.get('price')
            sale.save()

            return redirect('inventory_list')

        if request.POST.get('return'):
            sale = Sale.objects.select_related('inventory').get(id=request.POST.get('sale'))
            sale.is_active = False
            sale.save()

            sale.inventory.is_busy = 0
            sale.inventory.save()

            return redirect('inventory_list')

        else:
            inventory = Inventory.objects.get(id=request.POST.get('inventory'))
            inventory.is_busy = 2
            inventory.save()

        sale = Sale.objects.create(inventory=inventory, cost=request.POST['price'])

    if request.method == 'GET':
        if request.GET.get('sale_confirm'):
            pet = Inventory.objects.get(id=request.GET.get('sale_confirm'))

            return render(request, "sell/sell_pet.html", {'pet': pet, 'profile': profile})
        if request.GET.get('edit_details'):
            pet = Inventory.objects.get(id=request.GET.get('edit_details'))
            curr_sale = Sale.objects.select_related('inventory').exclude(is_active=False).get(inventory=pet)


            return render(request, "sell/return_pet.html", {'pet': curr_sale, 'profile': profile})


    return redirect('inventory_list')