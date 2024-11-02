from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from login_register.models import Profile
from inventory.models import Inventory, Pet
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse

# Create your views here.
@login_required
def user_profile(request):
    profile = Profile.objects.filter(user=request.user).first()

    total_pets = Inventory.objects.filter(owner_id=request.user.id).count()

    rarity_ctr = {
        'common': Inventory.objects.filter(owner_id=request.user.id, pet_id__rarity=Pet.Rarity.COMMON).count(),
        'uncommon': Inventory.objects.filter(owner_id=request.user.id, pet_id__rarity=Pet.Rarity.UNCOMMON).count(),
        'rare': Inventory.objects.filter(owner_id=request.user.id, pet_id__rarity=Pet.Rarity.RARE).count(),
        'mythical': Inventory.objects.filter(owner_id=request.user.id, pet_id__rarity=Pet.Rarity.MYTHICAL).count(),
    }

    rarity_bar = {
        key: (count / total_pets * 100) if total_pets > 0 else 0
        for key, count in rarity_ctr.items()
    }

    context = {
        'profile': profile,
        'total_pets': total_pets,
        'rarity_bar': rarity_bar,
    }

    return render(request, 'user_profile.html', context)


def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        profile.first_name = request.POST.get('first_name', profile.first_name)
        profile.last_name = request.POST.get('last_name', profile.last_name)

        username = request.POST.get('username', profile.user.username)

        if username != profile.user.username:
            profile.user.username = username
            profile.user.save()

        avatar_id = request.POST.get('inventory_id')
        if avatar_id:
            profile.avatar = avatar_id

        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return HttpResponseForbidden("Invalid request")

def delete_account(request):
    user = request.user
    user.delete()
    return redirect('landingpage')

def showcase_pet(request):
    return redirect('profile')

def update_showcase(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        inventory_id = data.get('inventory_id')
        inventory_item = get_object_or_404(Inventory, id=inventory_id, owner_id=request.user)
        profile = request.user.profile
        profile.showcased_pet = inventory_item
        profile.save()
        showcase_html = render_to_string('templates/showcased_pet.html', {'pet': inventory_item.pet_id})
        return JsonResponse({'success': True, 'showcase_html': showcase_html})