from django.shortcuts import render
from login_register.models import Profile

# Create your views here.
def base(request):
    profile = Profile.objects.filter(user=request.user).first() if request.user.is_authenticated else None
    print(profile)
    return render(request, "base.html", {'profile': profile})