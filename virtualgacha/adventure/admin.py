from django.contrib import admin
from .models import Adventure, AdventurePet, AdventureUser
# Register your models here.
admin.site.register(Adventure)
admin.site.register(AdventurePet)
admin.site.register(AdventureUser)