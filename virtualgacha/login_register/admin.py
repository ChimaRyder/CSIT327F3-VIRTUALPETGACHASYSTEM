from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'birthdate')

admin.site.register(Profile, ProfileAdmin)