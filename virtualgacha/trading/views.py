from PIL.ImageTransform import PerspectiveTransform
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from inventory.models import Inventory, Pet
from login_register.models import Profile
from trading.models import Trade


# Create your views here.

def trading_list(request):
    profile = Profile.objects.get(user=request.user)
    trades = Trade.objects.select_related('pet_to_trade__pet_id').exclude(pet_to_trade__owner_id=request.user)
    user_pets = Inventory.objects.filter(owner_id=request.user).filter(is_busy=Inventory.BusyValue.NOT_BUSY)
    pets = Pet.objects.all()

    if request.method == 'POST':
        preferences_array = []
        if request.POST.get('preferences'):
            preferences_array = request.POST.get('preferences').split(',')

        Trade.objects.create(
            pet_to_trade = Inventory.objects.get(id=request.POST.get('selected_pet')),
            pet_preferences=preferences_array,
        )


    return render(request, "trading_list.html", {'profile': profile, 'trading_list': trades, 'user_pets': user_pets, 'pets': pets})

def trade(request, trade_id):
    profile = Profile.objects.get(user=request.user)
    if Trade.objects.filter(id=trade_id).exists():
        trade_object = Trade.objects.get(id=trade_id)

        return render(request, "trade.html", {"trade": trade_object, "profile": profile})

    return render(request, "trade_not_exist.html", {"profile": profile})

def get_pet(request, pet_id):
    pet = get_object_or_404(Inventory, id=pet_id)

    pet_data = {
        "id" : pet.id,
        "species" : pet.pet_id.pet_species,
        "rarity" : pet.pet_id.rarity,
        "date_pulled" : pet.date_acquired,
        "rate" : pet.pet_id.pet_rate,
        "image_url" : pet.pet_id.pet_image.url,
    }

    return JsonResponse(pet_data)

