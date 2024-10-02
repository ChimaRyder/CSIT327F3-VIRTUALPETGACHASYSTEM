from django.contrib import admin

from .models import Inventory, Pet

# Register your models here.
admin.site.register(Inventory)
admin.site.register(Pet)