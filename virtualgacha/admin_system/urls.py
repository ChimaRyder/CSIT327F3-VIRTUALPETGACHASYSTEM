from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='admin_login'),
    path('dashboard/', views.dashboard_view, name='staff_dashboard'),
    path('pets/', views.pets_view, name='staff_pets'),
    path('logout/', views.logout_view, name='staff_logout'),
    path('users/', views.users_view, name='staff_users'),
    path('lootboxes/', views.lootboxes_view, name='staff_lootboxes'),
    path('marketplace/', views.marketplace_view, name='staff_marketplace'),
    path('transactions/', views.transactions_view, name='staff_transactions'),
    path('staff_pets/', views.query_pets, name='query_pets'),

    path('add_pet/', views.add_pet, name='add_pet'),
    path('edit_pet/<int:pet_id>/', views.edit_pet, name='edit_pet'),
    path('delete_pet/<int:pet_id>/', views.delete_pet, name='delete_pet'),
]