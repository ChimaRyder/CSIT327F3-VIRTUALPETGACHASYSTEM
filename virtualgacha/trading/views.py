from OpenSSL.rand import status
from PIL.ImageTransform import PerspectiveTransform
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from inventory.models import Inventory, Pet
from login_register.models import Profile
from notification.models import Notification
from trading.models import Trade


# Create your views here.

def trading_list(request):
    profile = Profile.objects.get(user=request.user)
    items_per_page = 5
    trades = Trade.objects.select_related('pet_to_trade__pet_id').exclude(pet_to_trade__owner_id=request.user).exclude(status=Trade.TradeStatus.success)
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

        pet = Inventory.objects.get(id=request.POST.get('selected_pet'))
        pet.is_busy = Inventory.BusyValue.BUSY
        pet.save()

    rarity_filter = []
    if request.method == 'GET':
        if request.GET.get('own_trades'):
            trades = Trade.objects.select_related('pet_to_trade__pet_id').filter(pet_to_trade__owner_id=request.user).exclude(status=Trade.TradeStatus.success)
        if request.GET.get('sort'):
            if request.GET.get('sort') == 'rarity_ascending':
                trades = trades.order_by('pet_to_trade__pet_id__rarity')
            if request.GET.get('sort') == 'rarity_descending':
                trades = trades.order_by('pet_to_trade__pet_id__rarity').reverse()
        if request.GET.get('rarity'):
            rarity_filter = request.GET.getlist('rarity')
            rarity_enum = ['Common', 'Uncommon', 'Rare', 'Mythical', 'Legendary']
            rarity_filter = [rarity_enum.index(r) for r in rarity_filter]
            trades = [trades for trades in trades if trades.pet_to_trade.pet_id.rarity in rarity_filter]
        if request.GET.get('q'):
            trades = [trades for trades in trades if trades.pet_to_trade.pet_id.pet_species.lower().startswith(request.GET.get('q').lower())]

    paginator = Paginator(trades, items_per_page)
    page = request.GET.get('page', 1)
    trades = paginator.get_page(page)

    return render(request, "trading_list.html", {'profile': profile, 'trading_list': trades, 'user_pets': user_pets, 'pets': pets, "rarity_selected": rarity_filter})

def trade(request, trade_id):
    profile = Profile.objects.get(user=request.user)
    user_pets = Inventory.objects.filter(owner_id=request.user).filter(is_busy=Inventory.BusyValue.NOT_BUSY)
    if Trade.objects.filter(id=trade_id).exists() and not Trade.objects.get(id=trade_id).status == Trade.TradeStatus.success:
        trade_object = Trade.objects.select_related("pet_to_offer").get(id=trade_id)

        if len(trade_object.pet_preferences) < 4:
            while len(trade_object.pet_preferences) < 4:
                trade_object.pet_preferences.append("x")

        if request.method == "POST" and "selected-offer" in request.POST:
            offer = Inventory.objects.get(id=request.POST.get('selected-offer'))
            offer.is_busy = Inventory.BusyValue.BUSY
            offer.save()
            trade_object.pet_to_offer = offer
            trade_object.status = Trade.TradeStatus.waiting
            trade_object.save()

            Notification.objects.create(
                user=trade_object.pet_to_trade.owner_id,
                title="Trade Request",
                text=f"{request.user} wants to trade with you. Check it out!",
                link=reverse("trade", kwargs={'trade_id': trade_object.id}),
            )

        elif request.method == "POST" and "trade-offer-status" in request.POST:
            if request.POST["trade-offer-status"] == "ACCEPTED":
                #close trade
                trade_object.status = Trade.TradeStatus.success
                trade_object.date_completed = timezone.now()
                trade_object.save()
                #notify other of accepted trade
                Notification.objects.create(
                    user = trade_object.pet_to_offer.owner_id,
                    title="Trade Accepted",
                    text=f"{request.user} has accepted your trade! Check your new pet in your inventory.",
                    link = reverse("inventory_list")
                )
                Notification.objects.create(
                    user = trade_object.pet_to_trade.owner_id,
                    title="Trade Accepted",
                    text=f"You have accepted {trade_object.pet_to_offer.owner_id.username}'s pet! Check your new pet in your inventory.",
                    link = reverse("inventory_list")
                )
                #swap pets
                x = trade_object.pet_to_trade.owner_id
                trade_object.pet_to_trade.owner_id = trade_object.pet_to_offer.owner_id
                trade_object.pet_to_offer.owner_id = x
                trade_object.pet_to_trade.save()
                trade_object.pet_to_offer.save()
                #remove is_busy
                trade_object.pet_to_trade.is_busy = Inventory.BusyValue.NOT_BUSY
                trade_object.pet_to_offer.is_busy = Inventory.BusyValue.NOT_BUSY
                trade_object.pet_to_trade.save()
                trade_object.pet_to_offer.save()

                return redirect("inventory_list")

            else:
                #make trade available
                trade_object.status = Trade.TradeStatus.available
                trade_object.save()
                #make offer not busy
                trade_object.pet_to_offer.is_busy = Inventory.BusyValue.NOT_BUSY
                trade_object.pet_to_offer.save()
                #notify other user
                Notification.objects.create(
                    user = trade_object.pet_to_offer.owner_id,
                    title="Trade Declined",
                    text=f"{request.user} has declined your trade. Would you like to make another trade?",
                    link = reverse("trade", kwargs={'trade_id': trade_object.id})
                )
                #make offer null
                trade_object.pet_to_offer = None
                trade_object.save()

        elif request.method == "POST" and "cancel-trade" in request.POST:
            #make the pet not busy
            trade_object.pet_to_trade.is_busy = Inventory.BusyValue.NOT_BUSY
            trade_object.pet_to_trade.save()
            #check if there's another pet, then turn it not busy
            if trade_object.pet_to_offer:
                trade_object.pet_to_offer.is_busy = Inventory.BusyValue.NOT_BUSY
                trade_object.pet_to_offer.save()
            #cancel the trade
            trade_object.status = Trade.TradeStatus.success
            trade_object.date_completed = timezone.now()
            trade_object.save()
            #redirect to trade list
            return redirect("inventory_list")

        return render(request, "trade.html", {"trade": trade_object, "profile": profile, "pets": user_pets})

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

