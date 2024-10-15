from django.shortcuts import render, get_object_or_404
from .models import Lootbox

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

    context = {
        'lootbox': lootbox,
    }

    return render(request, "lootbox_ui.html", context)