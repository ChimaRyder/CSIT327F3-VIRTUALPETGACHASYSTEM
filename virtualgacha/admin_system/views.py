from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from inventory.models import *
from django.contrib import messages
from django.http import JsonResponse
from inventory.models import *
from login_register.models import *
from lootbox_market.models import * 
from checkout_system.models import *
from notification.models import *
from marketplace.models import *
from django.db.models import Sum
from adventure.models import *
from trading.models import *
from chat.models import *
from daily_rewards.models import *
import random
import json

def is_staff(user):
    return user.is_staff

def login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('staff_dashboard')

    if not request.user.is_staff:
        messages.error(request, 'You are not authorized to access this page.')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                try:
                    Reward.objects.create(
                        credit_reward=random.randint(50, 500),
                    )
                except Exception as e:
                    print(e)

                login(request, user)
                return redirect('staff_dashboard')
            else:
                messages.error(request, 'You are not authorized to access this page.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'staff_login.html')

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def query_pets(request):
    query = request.GET.get('search', '')
    filter_by = request.GET.get('filter', '')
    sort_by = request.GET.get('sort', '')

    pets = Pet.objects.all()

    if query:
        if filter_by == 'pet_id':
            pets = pets.filter(id=query)
        elif filter_by == 'pet_species':
            pets = pets.filter(pet_species__icontains=query)
        elif filter_by == 'rarity':
            pets = pets.filter(rarity=query)
        elif filter_by == 'pet_rate':
            pets = pets.filter(pet_rate=query)

    if filter_by:
        if filter_by == 'pet_species':
            pets = pets.order_by('pet_species')
        elif filter_by == 'rarity':
            pets = pets.order_by('rarity')
        elif filter_by == 'pet_rate':
            pets = pets.order_by('pet_rate')

    if sort_by == 'descending':
        pets = pets.reverse()

    paginator = Paginator(pets, 10)  # Show 10 pets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    rarity_choices = Pet.Rarity.choices

    return render(request, 'staff_pets.html', {'page_obj': page_obj, 'rarity_choices': rarity_choices})

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def dashboard_view(request):
    total_pulls = Pull.objects.count()
    total_adventures = Adventure.objects.count()
    total_money_spent_lootbox = Pull.objects.aggregate(total_cost=Sum('lootbox_id__rate_cost'))['total_cost'] or 0
    total_money_spent_marketplace = Purchase.objects.filter(sale__is_active=False).aggregate(total_cost=Sum('sale__cost'))['total_cost'] or 0
    total_money_spent_transactions = Transaction.objects.filter(status='SUCCESS', transaction_type='BUY').aggregate(total_cost=Sum('total_changes'))['total_cost'] or 0
    total_sales_transactions = Transaction.objects.filter(status='SUCCESS', transaction_type='BUY').count()
    total_users = User.objects.count()
    notifications_list = Notification.objects.all().order_by('-created_at')
    pull_pets = PullPet.objects.select_related('pull_id').order_by('-pull_id__date_created')[:10]
    pull_pets_data = pull_pets.values('pull_id__user_id__username' , "pet_id__pet_species", 'pull_id', 'pull_id__lootbox_id__lootbox_name','pet_id', 'pull_id__date_created')

    print(pull_pets_data)

    context = {
        'notifications_list' : notifications_list[0:10],
        'total_pulls': total_pulls,
        'total_adventures': total_adventures,
        'total_money_spent_lootbox': total_money_spent_lootbox,
        'total_money_spent_marketplace': total_money_spent_marketplace,
        'total_money_spent_transactions': total_money_spent_transactions,
        'total_sales_transactions': total_sales_transactions,
        'total_users': total_users,
        'pulls_list' : pull_pets_data
    }

    return render(request, 'staff_dashboard.html', context)

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def make_announcement(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        claim_coins = request.POST.get('claim_coins', 0)

        users = User.objects.all()
        for user in users:
            Notification.objects.create(
                user=user,
                notif_status=Notification.Status.unread,
                title=title,
                text=text + f" - admin {request.user.username}",
                claim_coins=claim_coins
            )

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def pets_view(request):
    pets = Pet.objects.all()
    paginator = Paginator(pets, 10)  # Show 10 pets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    rarity_choices = Pet.Rarity.choices
    return render(request, 'staff_pets.html', {'page_obj': page_obj, 'rarity_choices': rarity_choices})

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def add_pet(request):
    if request.method == 'POST':
        pet_species = request.POST.get('pet_species')
        rarity = request.POST.get('rarity')
        pet_rate = request.POST.get('pet_rate')
        pet_image = request.FILES.get('pet_image')

        print("HELLO WORLD!", request.FILES)
        print("HELLO image!", pet_rate)

        pet = Pet(pet_species=pet_species, rarity=rarity, pet_rate=pet_rate, pet_image=pet_image)
        pet.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        pet.pet_species = request.POST.get('pet_species')
        pet.rarity = request.POST.get('rarity')
        pet.pet_rate = request.POST.get('pet_rate')

        if 'pet_image' in request.FILES:
            pet.pet_image = request.FILES.get('pet_image')
            # print(pet.pet_image)
        pet.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        pet.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# --- LOOTBOX ---
@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def get_pet_details(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return JsonResponse({'id': pet.id, 'pet_image' : pet.pet_image.url, 'pet_species': pet.pet_species, 'rarity': pet.rarity, 'pet_rate': pet.pet_rate})

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def lootbox_add_view(request):
    query = request.GET.get('search', '')
    filter_by = request.GET.get('filter', '')
    sort_by = request.GET.get('sort', '')

    pets = Pet.objects.all()

    if query:
        if filter_by == 'pet_id':
            pets = pets.filter(id=query)
        elif filter_by == 'pet_species':
            pets = pets.filter(pet_species__icontains=query)
        elif filter_by == 'rarity':
            pets = pets.filter(rarity=query)
        elif filter_by == 'pet_rate':
            pets = pets.filter(pet_rate=query)

    if filter_by:
        if filter_by == 'pet_species':
            pets = pets.order_by('pet_species')
        elif filter_by == 'rarity':
            pets = pets.order_by('rarity')
        elif filter_by == 'pet_rate':
            pets = pets.order_by('pet_rate')

    if sort_by == 'descending':
        pets = pets.reverse()

    paginator = Paginator(pets, 10)  # Show 10 pets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    rarity_choices = Pet.Rarity.choices

    return render(request, 'staff_lootboxes_add.html', {'page_obj': page_obj, 'rarity_choices': rarity_choices})


@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def query_lootboxes(request):
    query = request.GET.get('search', '')
    filter_by = request.GET.get('filter', '')
    sort_by = request.GET.get('sort', '')

    lootboxes = Lootbox.objects.all()

    if query:
        if filter_by == 'lootbox_id':
            lootboxes = lootboxes.filter(lootbox_id=query)
        elif filter_by == 'lootbox_name':
            lootboxes = lootboxes.filter(lootbox_name__icontains=query)
        elif filter_by == 'rate_cost':
            lootboxes = lootboxes.filter(rate_cost=query)
        elif filter_by == 'tagged_relevance':
            lootboxes = lootboxes.filter(tagged_relevance__icontains = query)
        elif filter_by == 'drop_box':
            lootboxes = lootboxes.filter(lootboxdroptable__pet_id__pet_species__icontains=query).distinct()

    if filter_by:
        if filter_by == 'lootbox_name':
            lootboxes = lootboxes.order_by('lootbox_name')
        elif filter_by == 'rate_cost':
            lootboxes = lootboxes.order_by('rate_cost')
        elif filter_by == 'tagged_relevance':
            lootboxes = lootboxes.order_by('tagged_relevance')
        elif filter_by == 'drop_box':
            lootboxes = lootboxes.order_by('lootboxdroptable__pet_id__pet_species')

    if sort_by == 'descending':
        lootboxes = lootboxes.reverse()

    paginator = Paginator(lootboxes, 10)  # Show 10 lootboxes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'staff_lootboxes.html', {'page_obj': page_obj})


@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def lootboxes_view(request):
    lootboxes = Lootbox.objects.all()
    paginator = Paginator(lootboxes, 10)  # Show 10 lootboxes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'staff_lootboxes.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def add_lootbox(request):
    if request.method == 'POST':
        lootbox_name = request.POST.get('lootbox_name')
        rate_cost = request.POST.get('rate_cost')
        image = request.FILES.get('image')
        pet_ids_str = request.POST.get('pet_ids')
        tagged_relevance = request.POST.get('tagged_relevance')

        # Convert the string representation of the list to an actual list
        pet_ids = json.loads(pet_ids_str)

        lootbox = Lootbox(tagged_relevance=tagged_relevance, lootbox_name=lootbox_name, rate_cost=rate_cost, image=image)
        lootbox.save()

        for pet_id in pet_ids:
            print(pet_id)
            pet = Pet.objects.get(id=int(pet_id))
            lootbox_drop_table = LootboxDropTable(lootbox_id=lootbox, pet_id=pet)
            lootbox_drop_table.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def edit_lootbox_view(request, lootbox_id):
    lootbox = get_object_or_404(Lootbox, lootbox_id=lootbox_id)
    if request.method == 'POST':
        try: 
            lootbox.lootbox_name = request.POST.get('lootbox_name')
            lootbox.rate_cost = request.POST.get('rate_cost')
            lootbox.tagged_relevance = request.POST.get('tagged_relevance')
            print("Tagged relevance: ", request.POST.get('tagged_relevance'))
            
            if 'image' in request.FILES:
                lootbox.image = request.FILES.get('image')
            lootbox.save()
        except Exception as e:
            return JsonResponse({'success': False, 'message' : str(e)})

        # Update drop table
        LootboxDropTable.objects.filter(lootbox_id=lootbox).delete()
        pet_ids_str = request.POST.get('pet_ids')
        pet_ids = json.loads(pet_ids_str)
        
        for pet_id in pet_ids:
            pet = Pet.objects.get(id=int(pet_id))
            lootbox_drop_table = LootboxDropTable(lootbox_id=lootbox, pet_id=pet)
            lootbox_drop_table.save()

        return JsonResponse({'success': True})

    pets = Pet.objects.all()
    drop_table_pets = lootbox.lootboxdroptable_set.all()
    return render(request, 'staff_lootboxes_edit.html', {
        'lootbox': lootbox,
        'pets': pets,
        'drop_table_pets': drop_table_pets
    })

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def delete_lootbox(request, lootbox_id):
    lootbox = get_object_or_404(Lootbox, lootbox_id=lootbox_id)
    if lootbox:
        lootbox.delete()
        return redirect('staff_lootboxes')
    return redirect('staff_lootboxes')

# -- INVENTORY --

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def query_inventory(request):
    query = request.GET.get('search', '')
    filter_by = request.GET.get('filter', '')
    sort_by = request.GET.get('sort', '')

    inventory_items = Inventory.objects.all()

    if query:
        if filter_by == 'inventory_id':
            inventory_items = inventory_items.filter(id=query)
        elif filter_by == 'pet_id':
            inventory_items = inventory_items.filter(pet_id__id=query)
        elif filter_by == 'owner_id':
            inventory_items = inventory_items.filter(owner_id__username__icontains=query)
        elif filter_by == 'is_busy':
            inventory_items = inventory_items.filter(is_busy=query)
        elif filter_by == 'date_acquired':
            inventory_items = inventory_items.filter(date_acquired__date=query)

    if filter_by:
        if filter_by == 'inventory_id':
            inventory_items = inventory_items.order_by('id')
        elif filter_by == 'pet_id':
            inventory_items = inventory_items.order_by('pet_id')
        elif filter_by == 'owner_id':
            inventory_items = inventory_items.order_by('owner_id')
        elif filter_by == 'is_busy':
            inventory_items = inventory_items.order_by('is_busy')
        elif filter_by == 'date_acquired':
            inventory_items = inventory_items.order_by('date_acquired')

    if sort_by == 'descending':
        inventory_items = inventory_items.reverse()

    paginator = Paginator(inventory_items, 10)  # Show 10 inventory items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'staff_inventory.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def add_inventory(request):
    if request.method == 'POST':
        pet_id = request.POST.get('pet_id')
        owner_id = request.POST.get('owner_id')
        is_busy = request.POST.get('is_busy')

        pet = Pet.objects.get(id=pet_id)
        owner = User.objects.get(id=owner_id)

        inventory_item = Inventory(pet_id=pet, owner_id=owner, is_busy=is_busy)
        inventory_item.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def delete_inventory(request, inventory_id):
    inventory_item = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        inventory_item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# -- USERS --
@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def query_users(request):
    query = request.GET.get('search', '')
    filter_by = request.GET.get('filter', 'user_id')
    sort_by = request.GET.get('sort', 'ascending')

    profiles = Profile.objects.all()

    if query:
        if filter_by == 'user_id':
            profiles = profiles.filter(user__id__icontains=query)
        elif filter_by == 'username':
            profiles = profiles.filter(user__username__icontains=query)
        elif filter_by == 'email':
            profiles = profiles.filter(user__email__icontains=query)
        elif filter_by == 'first_name':
            profiles = profiles.filter(first_name__icontains=query)
        elif filter_by == 'last_name':
            profiles = profiles.filter(last_name__icontains=query)
        elif filter_by == 'birthdate':
            profiles = profiles.filter(birthdate__icontains=query)
        elif filter_by == 'total_credits':
            profiles = profiles.filter(total_credits__icontains=query)

    if sort_by == 'ascending':
        profiles = profiles.order_by(f'user__{filter_by}' if filter_by in ['username', 'email'] else filter_by)
    elif sort_by == 'descending':
        profiles = profiles.order_by(f'-user__{filter_by}' if filter_by in ['username', 'email'] else f'-{filter_by}')

    paginator = Paginator(profiles, 5)  # Show 10 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'staff_users.html', {'page_obj': page_obj})

@login_required
@user_passes_test(login_url='admin_login', test_func=is_staff)
def edit_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)

        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.birthdate = request.POST.get('birthdate')
        profile.total_credits = request.POST.get('total_credits')
        # profile.following = request.POST.get('following')
        # profile.followers = request.POST.get('followers')
        profile.save()

        return redirect('staff_users')
    return redirect('staff_users')

@login_required
@user_passes_test(login_url='admin_login', test_func=is_staff)
def ban_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_active = False
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
@user_passes_test(login_url='admin_login', test_func=is_staff)
def unban_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
@user_passes_test(login_url='admin_login', test_func=is_staff)
def turn_admin(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_staff = True
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
@user_passes_test(login_url='admin_login', test_func=is_staff)
def revoke_admin(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_staff = False
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# -- TRADES --
@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def query_trades(request):
    query = request.GET.get('search', '')
    filter_by = request.GET.get('filter', '')
    sort_by = request.GET.get('sort', '')

    trades = Trade.objects.all()

    if query:
        if filter_by == 'trade_id':
            trades = trades.filter(id=query)
        elif filter_by == 'pet_to_trade':
            trades = trades.filter(pet_to_trade__pet_id__id=query)
        elif filter_by == 'pet_to_offer':
            trades = trades.filter(pet_to_offer__pet_id__id=query)
        elif filter_by == 'status':
            trades = trades.filter(status__icontains=query)
        elif filter_by == 'date_created':
            trades = trades.filter(date_created__date=query)
        elif filter_by == 'date_completed':
            trades = trades.filter(date_completed__date=query)
        elif filter_by == 'username':
            trades = trades.filter(pet_to_trade__owner_id__username__icontains=query)

    if filter_by:
        if filter_by == 'trade_id':
            trades = trades.order_by('id')
        elif filter_by == 'pet_to_trade':
            trades = trades.order_by('pet_to_trade')
        elif filter_by == 'pet_to_offer':
            trades = trades.order_by('pet_to_offer')
        elif filter_by == 'status':
            trades = trades.order_by('status')
        elif filter_by == 'date_created':
            trades = trades.order_by('date_created')
        elif filter_by == 'date_completed':
            trades = trades.order_by('date_completed')
        elif filter_by == 'username':
            trades = trades.order_by('pet_to_trade__owner_id__username')

    if sort_by == 'descending':
        trades = trades.reverse()


    paginator = Paginator(trades, 10)  # Show 10 trades per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'staff_trades.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def disable_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id)
    if request.method == 'POST':
        trade.status = Trade.TradeStatus.success
        trade.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# -- TRANSACTIONS --
@login_required
@user_passes_test(login_url='admin_login', test_func=is_staff)
def query_transactions(request):
    query = request.GET.get('search', '')
    filter_by = request.GET.get('filter', 'transaction_id')
    sort_by = request.GET.get('sort', 'ascending')

    transactions = Transaction.objects.all()

    if query:
        if filter_by == 'transaction_id':
            transactions = transactions.filter(transaction_id__icontains=query)
        elif filter_by == 'user_id':
            transactions = transactions.filter(user_id__icontains=query)
        elif filter_by == 'status':
            transactions = transactions.filter(status__icontains=query)
        elif filter_by == 'payment_method':
            transactions = transactions.filter(payment_method__icontains=query)
        elif filter_by == 'transaction_type':
            transactions = transactions.filter(transaction_type__icontains=query)
        elif filter_by == 'gcash_number':
            transactions = transactions.filter(gcash_details__gcash_number__icontains=query)
        elif filter_by == 'card_number':
            transactions = transactions.filter(card_details__card_number__icontains=query)

    if sort_by == 'ascending':
        transactions = transactions.order_by(filter_by)
    elif sort_by == 'descending':
        transactions = transactions.order_by(f'-{filter_by}')

    paginator = Paginator(transactions, 5)  # Show 10 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'staff_transactions.html', {'page_obj': page_obj})

login_required
@user_passes_test(login_url='admin_login', test_func=is_staff)
def approve_transaction(request, transaction_id):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
        transaction.status = 'SUCCESS'
        transaction.save()

        # Create notification
        user = get_object_or_404(User, id=transaction.user_id)

        profile = get_object_or_404(Profile, user=user)

        profile.total_credits -= transaction.credits_amount

        Notification.objects.create(
            user=user,
            title="Transaction Approved",
            text=f"Your transaction with ID {transaction.transaction_id} has been approved.",
            claim_coins=0,
        )

        profile.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
@user_passes_test(login_url='admin_login', test_func=is_staff)
def decline_transaction(request, transaction_id):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
        transaction.status = 'DECLINED'
        transaction.save()

        # Create notification
        user = get_object_or_404(User, id=transaction.user_id)
        Notification.objects.create(
            user=user,
            title="Transaction Declined",
            text=f"Your transaction with ID {transaction.transaction_id} has been declined.",
            claim_coins=0,
        )

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# -- MARKETPLACE --
@login_required
@user_passes_test(login_url='admin_login', test_func=is_staff)
def query_marketplace(request):
    query = request.GET.get('search', '')
    filter_by = request.GET.get('filter', 'id')
    sort_by = request.GET.get('sort', 'ascending')

    sales = Sale.objects.all()

    if query:
        if filter_by == 'id':
            sales = sales.filter(id__icontains=query)
        elif filter_by == 'pet_species':
            sales = sales.filter(inventory__pet_id__pet_species__icontains=query)
        elif filter_by == 'cost':
            sales = sales.filter(cost__icontains=query)
        elif filter_by == 'date_created':
            sales = sales.filter(date_created__icontains=query)
        elif filter_by == 'status':
            sales = sales.filter(is_active__icontains=query)
        elif filter_by == 'seller':
            sales = sales.filter(inventory__owner_id__username__icontains=query)

   
    if sort_by == 'ascending':
        if filter_by == 'seller':
            sales = sales.order_by('inventory__owner_id__username')
        else:
            sales = sales.order_by(filter_by)
    elif sort_by == 'descending':
        if filter_by == 'seller':
            sales = sales.order_by('-inventory__owner_id__username')
        else:
            sales = sales.order_by(f'-{filter_by}')

    paginator = Paginator(sales, 10)  # Show 10 sales per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'staff_marketplace.html', {'page_obj': page_obj})


@login_required
@user_passes_test(login_url='admin_login', test_func=is_staff)
def toggle_listing(request, sale_id):
    if request.method == 'POST':
        sale = get_object_or_404(Sale, id=sale_id)
        sale.is_active = not sale.is_active
        sale.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# -- MESSAGES -- 
@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def query_chats(request):
    query = request.GET.get('search', '')
    filter_by = request.GET.get('filter', '')
    sort_by = request.GET.get('sort', '')

    messages = Message.objects.all()

    if query:
        if filter_by == 'message_id':
            messages = messages.filter(id=query)
        elif filter_by == 'room':
            messages = messages.filter(room__name__icontains=query)
        elif filter_by == 'sender':
            messages = messages.filter(sender__username__icontains=query)
        elif filter_by == 'content':
            messages = messages.filter(content__icontains=query)
        elif filter_by == 'timestamp':
            messages = messages.filter(timestamp__date=query)

    if filter_by:
        if filter_by == 'message_id':
            messages = messages.order_by('id')
        elif filter_by == 'room':
            messages = messages.order_by('room')
        elif filter_by == 'sender':
            messages = messages.order_by('sender')
        elif filter_by == 'content':
            messages = messages.order_by('content')
        elif filter_by == 'timestamp':
            messages = messages.order_by('timestamp')

    if sort_by == 'descending':
        messages = messages.reverse()

    paginator = Paginator(messages, 10)  # Show 10 messages per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'staff_messages.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def view_message_content(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    return JsonResponse({
        'message_id': message.id,
        'room': message.room.name,
        'sender': message.sender.username,
        'content': message.content,
        'timestamp': message.timestamp
    })

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def delete_message(request, message_id):
    if request.method == 'POST':
        message = get_object_or_404(Message, id=message_id)
        message.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# -- ROOMS --
@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def query_staff_rooms(request):
    query = request.GET.get('search', '')
    filter_by = request.GET.get('filter', '')
    sort_by = request.GET.get('sort', '')

    staff_rooms = ChatRoom.objects.all()

    if query:
        if filter_by == 'id':
            staff_rooms = staff_rooms.filter(id=query)
        elif filter_by == 'type':
            staff_rooms = staff_rooms.filter(type__icontains=query)
        elif filter_by == 'name':
            staff_rooms = staff_rooms.filter(name__icontains=query)
        elif filter_by == 'members':
            staff_rooms = staff_rooms.annotate(member_count=models.Count('members')).filter(member_count=query)

    if filter_by:
        if filter_by == 'id':
            staff_rooms = staff_rooms.order_by('id')
        elif filter_by == 'type':
            staff_rooms = staff_rooms.order_by('type')
        elif filter_by == 'name':
            staff_rooms = staff_rooms.order_by('name')
        elif filter_by == 'members':
            staff_rooms = staff_rooms.annotate(member_count=models.Count('members')).order_by('member_count')

    if sort_by == 'descending':
        staff_rooms = staff_rooms.reverse()

    paginator = Paginator(staff_rooms, 10)  # Show 10 staff rooms per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'staff_rooms.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def delete_chat_room(request, room_id):
    if request.method == 'POST':
        room = get_object_or_404(ChatRoom, room_id=room_id)
        room.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# -- DAILY REWARDS --
@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def query_staff_rewards(request):
    query = request.GET.get('search', '')
    filter_by = request.GET.get('filter', '')
    sort_by = request.GET.get('sort', '')

    staff_rewards = Reward.objects.all()

    if query:
        if filter_by == 'date':
            staff_rewards = staff_rewards.filter(date=query)
        elif filter_by == 'credit_reward':
            staff_rewards = staff_rewards.filter(credit_reward=query)
        elif filter_by == 'pet_reward':
            staff_rewards = staff_rewards.filter(pet_reward__pet_species__icontains=query)

    if filter_by:
        if filter_by == 'date':
            staff_rewards = staff_rewards.order_by('date')
        elif filter_by == 'credit_reward':
            staff_rewards = staff_rewards.order_by('credit_reward')
        elif filter_by == 'pet_reward':
            staff_rewards = staff_rewards.order_by('pet_reward')

    if sort_by == 'descending':
        staff_rewards = staff_rewards.reverse()

    paginator = Paginator(staff_rewards, 10)  # Show 10 staff rewards per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'staff_rewards.html', {'page_obj': page_obj, 'pets': Pet.objects.all().order_by('pet_species')})


@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def edit_staff_reward(request, reward_id):
    reward = get_object_or_404(Reward, id=reward_id)
    if request.method == 'POST':
        # reward.date = request.POST.get('date')
        reward.credit_reward = request.POST.get('credit_reward')
        pet_id = request.POST.get('pet_reward')
        reward.pet_reward = Pet.objects.get(id=pet_id) if pet_id else None
        reward.save()
        return redirect('query_staff_rewards')
    return redirect('query_staff_rewards')

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def create_staff_reward(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        credit_reward = request.POST.get('credit_reward')
        pet_id = request.POST.get('pet_reward')
        pet_reward = Pet.objects.get(id=pet_id) if pet_id else None
        Reward.objects.create(date=date, credit_reward=credit_reward, pet_reward=pet_reward)
        return redirect('query_staff_rewards')
    return redirect('query_staff_rewards')

# OTHER SUTFF

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def logout_view(request):
    logout(request)
    return render(request, 'staff_login.html')

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def users_view(request):
    return render(request, 'staff_login.html')

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def marketplace_view(request):
    return render(request, 'staff_login.html')

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def lootboxes_view(request):
    return render(request, 'staff_lootboxes.html')

@login_required(login_url='admin_login')
@user_passes_test(login_url='admin_login', test_func=is_staff)
def transactions_view(request):
    return render(request, 'staff_login.html')
