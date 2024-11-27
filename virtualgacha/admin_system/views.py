from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from inventory.models import *
from django.contrib import messages
from django.http import JsonResponse
from inventory.models import Pet

def is_staff(user):
    return user.is_staff

def login_view(request):
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
    return render(request, 'staff_login.html')

@login_required(login_url='admin_login')
@user_passes_test(is_staff)
def transactions_view(request):
    return render(request, 'staff_login.html')
