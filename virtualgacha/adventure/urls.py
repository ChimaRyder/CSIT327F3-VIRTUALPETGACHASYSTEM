from django.urls import path
from .views import adventure_page, start_adventure, get_pet_info, callback_pet

urlpatterns = [
    path('', adventure_page, name='adventure'),
    path('start_adventure/', start_adventure, name='start_adventure'),
    path('get_pet_info/<int:pet_id>/', get_pet_info, name='get_pet_info'),
    path('callback_pet/', callback_pet, name='callback_pet'),
]