from django.urls import path
from . import views

urlpatterns = [
    path('', views.lootboxes, name='lootboxes'),
    path('<int:lootbox_id>/', views.lootbox_detail, name='lootbox_detail'),
    path('roll/<int:lootbox_id>/', views.roll_lootbox, name='roll_lootbox'),
]