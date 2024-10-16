from django.contrib import admin
from .models import Lootbox, LootboxHistory, LootboxDropTable, Pull, PullPet


# Register your models here.
admin.site.register(Lootbox)
admin.site.register(LootboxHistory)
admin.site.register(LootboxDropTable)
admin.site.register(Pull)
admin.site.register(PullPet)