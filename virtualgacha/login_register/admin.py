from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')

admin.site.unregister(User)
admin.site.register(User, UserAdmin) 