from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('process_transaction/', views.process_transaction, name='process_transaction'),
]