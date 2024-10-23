from django.shortcuts import render
from login_register.models import Profile

# Create your views here.
def adventure_page(request):
    profile = Profile.objects.filter(user=request.user).first()

    context = {
        'profile' : profile
    }
    

    return render(request, 'adventure_content.html', context)
