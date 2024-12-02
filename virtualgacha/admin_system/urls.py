from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='admin_login'),
    path('dashboard/', views.dashboard_view, name='staff_dashboard'),
    path('pets/', views.pets_view, name='staff_pets'),
    path('logout/', views.logout_view, name='staff_logout'),
    path('lootboxes/', views.query_lootboxes, name='staff_lootboxes'),
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

    path('users/', views.query_users, name='staff_users'),
    path('edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('ban/<int:user_id>/', views.ban_user, name='ban_user'),
    path('unban/<int:user_id>/', views.unban_user, name='unban_user'),
    path('turn_admin/<int:user_id>/', views.turn_admin, name='turn_admin'),
    path('revoke_admin/<int:user_id>/', views.revoke_admin, name='revoke_admin'),

    path('transactions/', views.query_transactions, name='staff_transactions'),
      path('transactions/approve/<int:transaction_id>/', views.approve_transaction, name='approve_transaction'),
    path('transactions/decline/<int:transaction_id>/', views.decline_transaction, name='decline_transaction'),

    path('marketplace/', views.query_marketplace, name='staff_marketplace'),
    path('toggle_listing/<int:sale_id>/', views.toggle_listing, name='toggle_listing'),

    path('make_announcement/', views.make_announcement, name='make_announcement'),

    path('trades/', views.query_trades, name='query_trades'),
    path('disable_trade/<int:trade_id>/', views.disable_trade, name='disable_trade'),

    path('chats/', views.query_chats, name='query_chats'),
    path('view_message_content/<int:message_id>/', views.view_message_content, name='view_message_content'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),

    path('chat_rooms/', views.query_staff_rooms, name='query_chat_rooms'),
    path('delete_chat_room/<int:room_id>/', views.delete_chat_room, name='delete_chat_room'),
]