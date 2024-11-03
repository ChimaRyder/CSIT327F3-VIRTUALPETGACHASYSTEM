from django.contrib import admin

from .models import Purchase, Sale

# Register your models here.
admin.site.register(Sale)
admin.site.register(Purchase)
