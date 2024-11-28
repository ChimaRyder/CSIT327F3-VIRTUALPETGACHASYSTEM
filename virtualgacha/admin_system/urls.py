from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='admin_login'),
    path('dashboard/', views.dashboard_view, name='staff_dashboard'),
    path('pets/', views.pets_view, name='staff_pets'),
    path('logout/', views.logout_view, name='staff_logout'),
    path('users/', views.users_view, name='staff_users'),
    path('lootboxes/', views.query_lootboxes, name='staff_lootboxes'),
    path('marketplace/', views.marketplace_view, name='staff_marketplace'),
    path('transactions/', views.transactions_view, name='staff_transactions'),
    path('lootboxes/add/', views.lootbox_add_view, name='lootboxes_add'),
    path('inventory/', views.query_inventory, name='query_inventory'),
    path('staff_pets/', views.query_pets, name='query_pets'),

    path('add_pet/', views.add_pet, name='add_pet'),
    path('edit_pet/<int:pet_id>/', views.edit_pet, name='edit_pet'),
    path('delete_pet/<int:pet_id>/', views.delete_pet, name='delete_pet'),
    path('get_pet/<int:pet_id>/', views.get_pet_details, name='get_pet_detail'),

    path('query_lootboxes/', views.query_lootboxes, name='query_lootboxes'),
    path('add_lootbox/', views.add_lootbox, name='add_lootbox'),
    path('lootboxes/edit/<int:lootbox_id>/', views.edit_lootbox_view, name='edit_lootbox'),
    path('delete_lootbox/<int:lootbox_id>/', views.delete_lootbox, name='delete_lootbox'),

    path('add_inventory/', views.add_inventory, name='add_inventory'),
    path('delete_inventory/<int:inventory_id>/', views.delete_inventory, name='delete_inventory'),
]