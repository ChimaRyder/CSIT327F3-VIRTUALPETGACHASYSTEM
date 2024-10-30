from django.shortcuts import render
from login_register.models import Profile
from chat.models import ChatRoom

# Create your views here.
def base(request):
    profile = Profile.objects.filter(user=request.user).first() if request.user.is_authenticated else None
    ChatRoom.objects.get_or_create(type='global', name='Global Chat')
    return render(request, "base.html", {'profile': profile})