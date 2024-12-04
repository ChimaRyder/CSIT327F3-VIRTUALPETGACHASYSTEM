from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from inventory.models import Inventory
from login_register.models import Profile
from marketplace.models import Sale, Purchase
from notification.models import Notification


# Create your views here.

@login_required(login_url='login')
def marketplace(request):
    items_per_page = 10
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        purchase = Sale.objects.select_related('inventory','inventory__owner_id__profile').get(id=request.POST.get('confirmed-purchase'))
        if purchase.inventory.is_busy == Inventory.BusyValue.ON_MARKET:
            profile = Profile.objects.get(user=user)

            if profile.total_credits >= purchase.cost:
                Purchase.objects.create(sale=purchase, buyer=user)
                profile.total_credits -= purchase.cost
                profile.save()

                # purchase.inventory.owner_id.profile.total_credits += purchase.cost
                # purchase.inventory.owner_id.profile.save()
                Notification.objects.create(
                    user=purchase.inventory.owner_id,
                    title="Sale Success",
                    text=f"Your pet has been successfully sold. You have earned {purchase.cost} coins.",
                    claim_coins=purchase.cost,
                )

                purchase.inventory.owner_id = user
                purchase.inventory.is_busy = 0
                # might change acquisition too we'll see
                purchase.inventory.save()

                purchase.is_active = False
                purchase.save()

                return render(request, 'purchase/purchase_successful.html', {'purchase': purchase, 'profile': profile})

            return render(request, 'purchase/insufficient_balance.html', {'purchase': purchase, 'profile': profile})
        return render(request, 'purchase/purchase_error.html', {'purchase': purchase, 'profile': profile})


    if Sale.objects.exclude(inventory__owner_id=user.id):
        sales = Sale.objects.select_related('inventory').exclude(inventory__owner_id=user.id).order_by('date_created')
        sales = sales.exclude(is_active=False)

        rarity_filter = []
        if request.method == 'GET':
            if request.GET.get('sort'):
                if request.GET.get('sort') == 'acquisition':
                    sales = sales.order_by('inventory__date_acquired')
                if request.GET.get('sort') == 'rarity_ascending':
                    sales = sales.order_by('inventory__pet_id__rarity')
                if request.GET.get('sort') == 'rarity_descending':
                    sales = sales.order_by('inventory__pet_id__rarity').reverse()
                if request.GET.get('sort') == 'price_ascending':
                    sales = sales.order_by('cost')
                if request.GET.get('sort') == 'price_descending':
                    sales = sales.order_by('cost').reverse()
            if request.GET.get('rarity'):
                rarity_filter = request.GET.getlist('rarity')
                rarity_enum = ['Common', 'Uncommon', 'Rare', 'Mythical', 'Legendary']
                rarity_filter = [rarity_enum.index(r) for r in rarity_filter]
                sales = [sales for sales in sales if sales.inventory.pet_id.rarity in rarity_filter]
            if request.GET.get('q'):
                sales = [sales for sales in sales if sales.inventory.pet_id.pet_species.lower().startswith(request.GET.get('q').lower())]
        total = len(sales)

        paginator = Paginator(sales, items_per_page)
        page = request.GET.get('page', 1)
        sales = paginator.page(page)

        return render(request, "marketplace/marketplace.html", {'sales' : sales, 'total': total, 'profile': profile, 'rarity_selected': rarity_filter})

    return render(request, "marketplace/marketplace.html", {'profile': profile})
