from django.contrib import admin

from .models import Inventory, Pets

# Register your models here.
admin.site.register(Inventory)
admin.site.register(Pets)