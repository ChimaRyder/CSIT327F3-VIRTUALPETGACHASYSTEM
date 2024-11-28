from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from inventory.models import *
from django.contrib import messages
from django.http import JsonResponse
from inventory.models import *
from lootbox_market.models import * 
import json

def is_staff(user):
    return user.is_staff

def login_view(request):
    if request.user.is_authenticated:
        return redirect('staff_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('staff_dashboard')
            else:
                messages.error(request, 'You are not authorized to access this page.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'staff_login.html')

@login_required(login_url='admin_login')
@user_passes_test(is_staff)
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
@user_passes_test(is_staff)
def dashboard_view(request):
    return render(request, 'staff_dashboard.html')

@login_required(login_url='admin_login')
@user_passes_test(is_staff)
def pets_view(request):
    pets = Pet.objects.all()
    paginator = Paginator(pets, 10)  # Show 10 pets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    rarity_choices = Pet.Rarity.choices
    return render(request, 'staff_pets.html', {'page_obj': page_obj, 'rarity_choices': rarity_choices})

@login_required(login_url='admin_login')
@user_passes_test(is_staff)
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
@user_passes_test(is_staff)
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
@user_passes_test(is_staff)
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        pet.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# --- LOOTBOX ---
@login_required(login_url='admin_login')
@user_passes_test(is_staff)
def get_pet_details(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return JsonResponse({'id': pet.id, 'pet_image' : pet.pet_image.url, 'pet_species': pet.pet_species, 'rarity': pet.rarity, 'pet_rate': pet.pet_rate})

@login_required(login_url='admin_login')
@user_passes_test(is_staff)
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
@user_passes_test(is_staff)
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
@user_passes_test(is_staff)
def lootboxes_view(request):
    lootboxes = Lootbox.objects.all()
    paginator = Paginator(lootboxes, 10)  # Show 10 lootboxes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'staff_lootboxes.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
@user_passes_test(is_staff)
def add_lootbox(request):
    if request.method == 'POST':
        lootbox_name = request.POST.get('lootbox_name')
        rate_cost = request.POST.get('rate_cost')
        image = request.FILES.get('image')
        pet_ids_str = request.POST.get('pet_ids')

        # Convert the string representation of the list to an actual list
        pet_ids = json.loads(pet_ids_str)

        lootbox = Lootbox(lootbox_name=lootbox_name, rate_cost=rate_cost, image=image)
        lootbox.save()

        for pet_id in pet_ids:
            print(pet_id)
            pet = Pet.objects.get(id=int(pet_id))
            lootbox_drop_table = LootboxDropTable(lootbox_id=lootbox, pet_id=pet)
            lootbox_drop_table.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required(login_url='admin_login')
@user_passes_test(is_staff)
def edit_lootbox_view(request, lootbox_id):
    lootbox = get_object_or_404(Lootbox, lootbox_id=lootbox_id)
    if request.method == 'POST':
        lootbox.lootbox_name = request.POST.get('lootbox_name')
        lootbox.rate_cost = request.POST.get('rate_cost')
        if 'image' in request.FILES:
            lootbox.image = request.FILES.get('image')
        lootbox.save()

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
@user_passes_test(is_staff)
def delete_lootbox(request, lootbox_id):
    lootbox = get_object_or_404(Lootbox, lootbox_id=lootbox_id)
    if request.method == 'POST':
        lootbox.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# -- INVENTORY --

@login_required(login_url='admin_login')
@user_passes_test(is_staff)
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
@user_passes_test(is_staff)
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
@user_passes_test(is_staff)
def delete_inventory(request, inventory_id):
    inventory_item = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        inventory_item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# OTHER SUTFF

@login_required(login_url='admin_login')
@user_passes_test(is_staff)
def logout_view(request):
    logout(request)
    return render(request, 'staff_login.html')

@login_required(login_url='admin_login')
@user_passes_test(is_staff)
def users_view(request):
    return render(request, 'staff_login.html')

@login_required(login_url='admin_login')
@user_passes_test(is_staff)
def marketplace_view(request):
    return render(request, 'staff_login.html')

@login_required(login_url='admin_login')
@user_passes_test(is_staff)
def lootboxes_view(request):
    return render(request, 'staff_lootboxes.html')

@login_required(login_url='admin_login')
@user_passes_test(is_staff)
def transactions_view(request):
    return render(request, 'staff_login.html')
