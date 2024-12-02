from django.urls import path

from trading import views

urlpatterns = [
    path('list/', views.trading_list, name='trading_list'),
    path('<int:trade_id>/', views.trade, name='trade'),
    path('get_pet/<int:pet_id>/', views.get_pet, name='get_pet'),
]