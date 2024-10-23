from django.urls import path
from . import views

urlpatterns = [
    path('', views.adventure_page, name='adventure'),
]