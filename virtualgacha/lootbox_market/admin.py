from django.contrib import admin
from .models import Lootbox, LootboxDropTable, Pull, PullPet


# Register your models here.
admin.site.register(Lootbox)
admin.site.register(LootboxDropTable)
admin.site.register(Pull)
admin.site.register(PullPet)