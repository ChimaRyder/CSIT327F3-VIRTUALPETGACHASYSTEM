from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('sell_pet/', views.sell_pet, name='sell_pet'),
]