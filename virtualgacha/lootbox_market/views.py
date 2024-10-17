from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from inventory.models import *
from django.http import JsonResponse
from django.core.paginator import Paginator
import random

# Create your views here
def human_readable_format(value):
    if value >= 1_000_000:
        return f'{value / 1_000_000:.1f}M'
    elif value >= 1_000:
        return f'{value / 1_000:.1f}K'
    else:
        return str(value)

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
def lootbox_detail(request, lootbox_id):
    lootbox = get_object_or_404(Lootbox, pk=lootbox_id)
    lootbox_history = Pull.objects.filter(lootbox_id=lootbox_id)
    lootbox_drop_table = LootboxDropTable.objects.filter(lootbox_id=lootbox_id)

    drop_table = []

    for item in lootbox_drop_table:
        drop_table.append(item.pet_id)

    drop_table = sorted(drop_table, key=lambda x: x.rarity, reverse=True)

    total_global_spent = sum([pull.get_total_spent() for pull in lootbox_history])

    total_users = len(set([pull.user_id for pull in lootbox_history]))

    # Pagination
    paginator = Paginator(lootbox_history, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for pull in page_obj:
        print(pull)
        # for history in pull:
            # print(history)

    context = {
        'lootbox': lootbox,
        'lootbox_history': lootbox_history,
        'lootbox_drop_table' : drop_table,
        'user_lootbox_history': Pull.objects.filter(user_id=request.user, lootbox_id=lootbox_id),
        'total_global_spent': human_readable_format(total_global_spent),
        'total_users': human_readable_format(total_users),
        'page_obj': page_obj,
    }

    return render(request, "lootbox_ui.html", context)


@login_required(login_url="/login/")
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

    print(user)

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
        Inventory.objects.create(pet_id=pet, owner_id=user)
    
    return JsonResponse({'results': results})