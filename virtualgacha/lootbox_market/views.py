from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.decorators.http import require_POST
from inventory.models import Pet
from django.http import JsonResponse
import random

# Create your views here
def lootboxes(request):
     # Query the database to get all lootboxes
    all_lootboxes = Lootbox.objects.all()
    
    # Categorize lootboxes based on tagged_relevance
    popular_items = all_lootboxes.filter(tagged_relevance=Lootbox.TaggedRelevance.POPULAR)
    recent_items = all_lootboxes.filter(tagged_relevance=Lootbox.TaggedRelevance.RECENT)
    featured_items = all_lootboxes.filter(tagged_relevance=Lootbox.TaggedRelevance.FEATURED)
    
    # Pass the categorized lootboxes to the template context
    context = {
        'popular_items': popular_items,
        'recent_items': recent_items,
        'featured_items': featured_items,
    }

    print(popular_items)
    print(recent_items)
    print(featured_items)

    return render(request, "market_lootbox_content.html", context)

def lootbox_detail(request, lootbox_id):
    lootbox = get_object_or_404(Lootbox, pk=lootbox_id)
    lootbox_history = LootboxHistory.objects.filter(lootbox_id=lootbox_id)
    lootbox_drop_table = LootboxDropTable.objects.filter(lootbox_id=lootbox_id)

    drop_table = []

    for item in lootbox_drop_table:
        drop_table.append(item.pet_id)

    drop_table = sorted(drop_table, key=lambda x: x.rarity, reverse=True)

    context = {
        'lootbox': lootbox,
        'lootbox_history': lootbox_history,
        'lootbox_drop_table' : drop_table,
    }

    return render(request, "lootbox_ui.html", context)



@require_POST
def roll_lootbox(request, lootbox_id):
    lootbox = get_object_or_404(Lootbox, pk=lootbox_id)
    rolls = int(request.POST.get('rolls', 1))
    lootbox_drop_table = LootboxDropTable.objects.filter(lootbox_id=lootbox_id)

    drop_table = []

    for item in lootbox_drop_table:
        drop_table.append(item.pet_id)
    
    results = []
    user = request.user

    # Create a new pull
    pull = Pull.objects.create(user_id=user, roll_info=rolls, lootbox_id=lootbox)

    for _ in range(rolls):
        pet = random.choice(drop_table)
        results.append({
            'name': pet.pet_species,
            'rarity': pet.get_rarity_display(),
            'image_url': str(pet.pet_image.url),
        })
        # Create a new PullPet entry
        PullPet.objects.create(pull_id=pull, pet_id=pet)
    
    return JsonResponse({'results': results})