import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from leaderboard.models import Leaderboard
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignupForm, LoginForm
from chat.models import ChatRoom
from daily_rewards.models import Reward
from .models import Profile, get_random_avatar

# Create your views here.
def landingpage_view(request):
    ChatRoom.objects.get_or_create(type='global', name='Global Chat')

    if request.user.is_authenticated:
        return redirect('lootboxes')
    
    return render(request, 'login_register/landing_page.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('lootboxes')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            user.first_name = form.cleaned_data['first_name'].capitalize()
            user.last_name = form.cleaned_data['last_name'].capitalize()
            
            user.save()
            
            leaderboard_entry, created = Leaderboard.objects.get_or_create(user=user)
            leaderboard_entry.save()
            
            
            Profile.objects.create(user=user, first_name=user.first_name, last_name=user.last_name)
            
            messages.success(request, "Successfully registered!")
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = SignupForm()

    return render(request, 'login_register/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('lootboxes')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('lootboxes')
    else:
        form = LoginForm()

    try:
        Reward.objects.create(
            credit_reward=random.randint(50, 500),
        )
    except Exception as e:
        print(e)

    
    return render(request, 'login_register/login.html', {'form': form})