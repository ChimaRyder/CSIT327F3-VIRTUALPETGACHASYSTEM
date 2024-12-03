from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from login_register.models import Profile
from inventory.models import Inventory, Pet
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.core.paginator import Paginator
from .achievements import achievements
from .models import UserAchievements
from django.contrib.auth import update_session_auth_hash

# Create your views here.
@login_required(login_url='login')
def user_profile(request, username=None):
    if username:
        profile = get_object_or_404(Profile, user__username=username)
    else:
        profile = get_object_or_404(Profile, user=request.user)
    
    
    full_name = f"{profile.first_name} {profile.last_name}"
    is_own_profile = request.user == profile.user

    pets = Inventory.objects.select_related('pet_id').filter(owner_id=request.user.id)
    showcased_pets = profile.showcased_pets.all()
    total_pets, rarity_ctr, rarity_bar = rarity_stats(request.user.id)

    filtered_rarity = request.GET.get('rarity', 'all')
    pets = rarity_filter(pets, filtered_rarity)

    achievement_types = list(achievements.keys())
    curr_page = achievement_pages(request, achievement_types)
    current_category = curr_page.object_list[0]
    category_achievements = achievements[current_category]

    unlocked_achievements = check_achievements(request.user)

    context = {
        'profile': profile,
        'is_own_profile': is_own_profile,
        'fullname': full_name,
        'total_pets': total_pets,
        'rarity_bar': rarity_bar,
        'rarity_ctr': rarity_ctr,
        'pets': pets,
        'showcased_pets': showcased_pets,
        'filtered_rarity': filtered_rarity,
        "current_category": current_category,
        "category_achievements": category_achievements,
        "paginator": curr_page.paginator,
        "curr_page": curr_page,
        "unlocked_achievements": unlocked_achievements,
    }
    
    return render(request, 'user_profile/user_profile.html', context)


def edit_profile(request):
    profile = Profile.objects.get(user=request.user) 

    if request.method == 'POST':
        profile.first_name = request.POST.get('first_name', profile.first_name)
        profile.last_name = request.POST.get('last_name', profile.last_name)
        username = request.POST.get('username', profile.user.username)

        curr_password = request.POST.get('curr_password')
        if curr_password and not request.user.check_password(curr_password):
            messages.error(request, "The current password is incorrect.")
            return redirect('user_profile:profile')

        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm-password')
        if new_password and new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('user_profile:profile')

        if username != profile.user.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken. Please enter a different one.", extra_tags="username_error")
                return redirect('user_profile:profile')

            profile.user.username = username
            profile.user.save()

        if 'avatar' in request.POST:
            profile.avatar = request.POST['avatar']
            profile.uploaded_avatar = None

        if 'uploaded_avatar' in request.FILES:
            profile.uploaded_avatar = request.FILES['uploaded_avatar']
            profile.avatar = None

        if new_password:
            profile.user.set_password(new_password)
            profile.user.save()
            update_session_auth_hash(request, profile.user) 

        profile.save()
        messages.success(request, "Your profile has been successfully updated!")
        return redirect('user_profile:profile')

    return HttpResponseForbidden("Invalid request")


def delete_account(request):
    user = request.user
    user.delete()
    return redirect('landingpage')

def rarity_stats(user_id):
    total_pets = Inventory.objects.filter(owner_id=user_id).count()

    rarity_ctr = {
        'common': Inventory.objects.filter(owner_id=user_id, pet_id__rarity=Pet.Rarity.COMMON).count(),
        'uncommon': Inventory.objects.filter(owner_id=user_id, pet_id__rarity=Pet.Rarity.UNCOMMON).count(),
        'rare': Inventory.objects.filter(owner_id=user_id, pet_id__rarity=Pet.Rarity.RARE).count(),
        'mythical': Inventory.objects.filter(owner_id=user_id, pet_id__rarity=Pet.Rarity.MYTHICAL).count(),
        'legendary': Inventory.objects.filter(owner_id=user_id, pet_id__rarity=Pet.Rarity.LEGENDARY).count(),
    }

    rarity_bar = {
        key: (count / total_pets * 100) if total_pets > 0 else 0
        for key, count in rarity_ctr.items()
    }

    return total_pets, rarity_ctr, rarity_bar


def rarity_filter(pets, rarity):
    if rarity == 'all':
        return pets
    
    rarity_filters = {
        'common': 0,
        'uncommon': 1,
        'rare': 2,
        'mythical': 3,
        'legendary': 4,
    }

    return pets.filter(pet_id__rarity=rarity_filters.get(rarity))


def showcase_pet(request, pet_id):
    if request.method == 'POST':
        profile = request.user.profile

        if profile.showcased_pets.all().count() >= 5:
            messages.error(request, "You can only showcase up to 5 pets.", extra_tags="showcase_error")
            return redirect('user_profile:profile')

        pet = get_object_or_404(Inventory, id=pet_id,  owner_id=request.user)
        profile.showcased_pets.add(pet)
        profile.save()
        return redirect('user_profile:profile')


def unshowcase_pet(request, pet_id):
    if request.method == 'POST':
        profile = request.user.profile
        pet = get_object_or_404(Inventory, id=pet_id, owner_id=request.user)
        profile.showcased_pets.remove(pet)
        profile.save()
        return redirect('user_profile:profile')


def achievement_pages(request, achievement_types):
    paginator = Paginator(achievement_types, 1)
    page_num = int(request.GET.get("page", 1))

    if page_num < 1:
        page_num = paginator.num_pages
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages

    return paginator.get_page(page_num)

def check_achievements(user):
    unlocked_achievements = []

    for category, achievements_list in achievements.items():
        for achievement in achievements_list:
            if achievement["condition"](user):
                if not UserAchievements.objects.filter(user=user, achievement_name=achievement["name"]).exists():
                    UserAchievements.objects.create(user=user, achievement_name=achievement["name"])
                    
                unlocked_achievements.append({
                    "category": category,
                    "name": achievement["name"],
                    "description": achievement["description"],
                    "badge": achievement["badge"],
                })

    return unlocked_achievements