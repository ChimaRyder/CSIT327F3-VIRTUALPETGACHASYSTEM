from django.shortcuts import render, redirect
from django.http import JsonResponse
from login_register.models import Profile
from .models import Adventure, AdventureUser, AdventurePet
from inventory.models import Pet, Inventory  # Assuming Pet and Inventory models are in the inventory app
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
from django.core.paginator import Paginator
import json
import re
import math
import random

# Create your views here.
@login_required
def adventure_page(request):
    profile = Profile.objects.filter(user=request.user).first()
    inventory_items = Inventory.objects.filter(owner_id=request.user, is_busy=Inventory.BusyValue.NOT_BUSY)
    is_busy = any(item.is_busy for item in inventory_items)

    # Get adventure history for the user, ordered by date_started descending
    adventure_history_list = AdventureUser.objects.filter(user_id=request.user, adventure_id__is_finished=True).order_by('-adventure_id__date_started')
    paginator = Paginator(adventure_history_list, 10)  # Show 10 adventures per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get total earnings for the user
    total_earnings = sum(adventure.adventure_id.total_earnings for adventure in adventure_history_list)

    # Get total runs for the user
    total_runs = adventure_history_list.count()

    # Get the current running adventure for the user
    current_adventure_user = AdventureUser.objects.filter(user_id=request.user, adventure_id__is_claimed=False).first()
    current_adventure = None
    if current_adventure_user:
        adventure_pet = AdventurePet.objects.filter(adventure_id=current_adventure_user.adventure_id).first()
        pet = adventure_pet.pet_id
        adventure = current_adventure_user.adventure_id

        # Calculate the duration in hours
        now = datetime.now(timezone.utc)
        duration = (now - adventure.date_started).total_seconds() / 3600

        # Calculate the earnings
        earnings = duration * adventure_pet.rate_multiplier

        # Check if the adventure should be auto-claimed
        if now >= adventure.date_finish:
            duration = (adventure.date_finish - adventure.date_started).total_seconds() / 3600
            finished_earnings = earnings + random.randint(1, math.ceil(duration) * 5)
            adventure.is_finished = True
            adventure.is_claimed = True
            adventure.total_earnings = finished_earnings
            adventure.save()
            
            inventory_item = Inventory.objects.get(pet_id=pet, owner_id=request.user, is_busy=Inventory.BusyValue.BUSY)
            inventory_item.is_busy = Inventory.BusyValue.NOT_BUSY
            inventory_item.save()

            # Update the total earnings for the user
            profile.total_credits += finished_earnings
            profile.save()

        current_adventure = {
            'adventure': adventure,
            'pet': pet,
            'rate_multiplier': adventure_pet.rate_multiplier,
            'earnings': earnings,
        }




    context = {
        'profile': profile,
        'user_inventory': inventory_items,
        'is_busy': is_busy,
        'adventure_history': page_obj,
        'current_adventure': current_adventure,
        'total_earnings': total_earnings,
        'total_runs': total_runs,
    }

    
    return render(request, 'adventure_content.html', context)

@login_required
def start_adventure(request):
    if request.method == 'POST':
        inventory_id = request.POST.get('inventory_id')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        print(inventory_id)

        # match = re.search(r'\((\d+)\)', inventory_id)

        inventory_item = Inventory.objects.get(id=inventory_id)


        pet = inventory_item.pet_id
        user = request.user

        # Parse the start and end times
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)

        # Calculate the duration in hours
        duration = (end_time - start_time).total_seconds() / 3600

        # Example rate multiplier, you can customize this
        rate_multiplier = pet.pet_rate 

        # Calculate the rate on finish
        rate_on_finish = duration * rate_multiplier

        # Create a new adventure
        adventure = Adventure.objects.create(
            date_started=start_time,
            date_finish=end_time
        )

        # Create a new AdventurePet entry
        AdventurePet.objects.create(
            adventure_id=adventure,
            pet_id=pet,
            rate_multiplier=rate_multiplier,
            rate_on_finish=rate_on_finish
        )

        # Create a new AdventureUser entry
        AdventureUser.objects.create(
            adventure_id=adventure,
            user_id=user
        )

        # Mark the pet as busy in the inventory
        inventory_item.is_busy = Inventory.BusyValue.BUSY
        inventory_item.save()

        return redirect('adventure')

    return redirect('adventure')

@login_required
def get_pet_info(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    data = {
        'rate': pet.pet_rate,
    }
    return JsonResponse(data)

@login_required
def callback_pet(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        adventure_id = data.get('adventure_id')

        adventure = Adventure.objects.get(adventure_id=adventure_id)

        adventure_pet = AdventurePet.objects.get(adventure_id=adventure)
        pet = adventure_pet.pet_id

        # Calculate the duration in hours
        now = datetime.now(timezone.utc)
        duration = (now - adventure.date_started).total_seconds() / 3600

        # Calculate the earnings
        earnings = duration * pet.pet_rate

        print(f'Earnings: {earnings}')

        # Update the total earnings for the user
        profile = Profile.objects.get(user=request.user)
        profile.total_credits += earnings
        profile.save()

        adventure = Adventure.objects.get(adventure_id=adventure_id)
        adventure.is_finished = True
        adventure.is_claimed = True
        adventure.date_finish = datetime.now(timezone.utc)
        adventure.total_earnings = earnings
        adventure.save()

        # Mark the pet as not busy in the inventory
        inventory_item = Inventory.objects.get(pet_id=pet, owner_id=request.user, is_busy=Inventory.BusyValue.BUSY)
        inventory_item.is_busy = Inventory.BusyValue.NOT_BUSY
        inventory_item.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})