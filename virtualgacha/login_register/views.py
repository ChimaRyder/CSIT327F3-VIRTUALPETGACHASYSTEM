from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import SignupForm, LoginForm


# Create your views here.
def landingpage_view(request):
    if request.user.is_authenticated:
        return redirect('lootboxes')
    return render(request, 'landing_page.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('lootboxes')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            #Profile.objects.get_or_create(user=user)
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

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
    
    return render(request, 'login.html', {'form': form})