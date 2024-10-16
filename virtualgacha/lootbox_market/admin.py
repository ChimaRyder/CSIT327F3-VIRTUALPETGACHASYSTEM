from django.contrib import admin
from .models import Lootbox, LootboxHistory, LootboxDropTable


# Register your models here.
admin.site.register(Lootbox)
admin.site.register(LootboxHistory)
admin.site.register(LootboxDropTable)
