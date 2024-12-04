from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from login_register.models import Profile
from inventory.models import Inventory
from marketplace.models import Sale
from user_profile.models import UserAchievements
from math import log
from .models import Leaderboard

# Create your views here.
@login_required(login_url='login')
def leaderboards_view(request):
    curr_prof = request.user.username
    profiles = Profile.objects.all()
    leaderboard_data = []

    leaderboard_entry, created = Leaderboard.objects.get_or_create(user=request.user)
    

    for profile in profiles:
        points = calculate_player_points(profile)
        avatar_url = profile.get_profile_image_url
        full_name = f"{profile.user.first_name} {profile.user.last_name}"

        total_pets = Inventory.objects.filter(owner_id=profile.user).count()

        leaderboard_entry, created = Leaderboard.objects.get_or_create(user=profile.user)
        leaderboard_entry.points = points
        leaderboard_entry.save()

        leaderboard_data.append((full_name, profile.user.username, points, avatar_url, leaderboard_entry, total_pets))

    leaderboard_data.sort(key=lambda x: x[2], reverse=True)

    for idx, entry in enumerate(leaderboard_data):
        leaderboard_entry = Leaderboard.objects.get(user__username=entry[1])
        leaderboard_entry.rank = idx + 1  # Rank starts at 1
        leaderboard_entry.save()
        
    top3 = leaderboard_data[:3]  
    rest_lead = leaderboard_data[3:]

    context = {
        'top3': top3,
        'rest_lead': rest_lead[:47],
        'profiles': profiles,
        'curr_prof': curr_prof,
        'leaderboard_data': leaderboard_data,
    }

    return render(request, 'leaderboard/leaderboard.html', context)



def calculate_player_points(profile):
    total_credits = profile.total_credits
    credits_score = log(total_credits + 1)
    
    pets = Inventory.objects.filter(owner_id=profile.user)

    rarity_points = {
        0: 1,
        1: 2,
        2: 4,
        3: 8,
        4: 16,
    }

    total_rarity = sum([rarity_points.get(pet.pet_id.rarity, 0) for pet in pets if pet.pet_id])
    avg_pet_rarity = total_rarity / len(pets) if pets.exists() else 0

    successful_sales = Sale.objects.filter(inventory__owner_id=profile.user, is_active=False).count()
    unsuccessful_sales_penalty = Sale.objects.filter(inventory__owner_id=profile.user, is_active=True).count()

    achievements_achieved = UserAchievements.objects.filter(user=profile.user).count() * 2
    # achievements_achieved = (profile.user.achievements.count()) * 2

    C1, C2, C3, C4, C5 = 1, 3, 3, 2, 1
    
    points = (
        C1 * credits_score +
        C2 * avg_pet_rarity +
        C3 * achievements_achieved +
        C4 * successful_sales - 
        C5 * unsuccessful_sales_penalty)
    
    return int(round(points))