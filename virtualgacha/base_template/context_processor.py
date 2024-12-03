from login_register.models import Profile

def profile_context(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user = request.user)
            return {'navbar_profile': profile}
        except Profile.DoesNotExist:
            return {'navbar_profile': None}
        
    return {'navbar_profile': None}