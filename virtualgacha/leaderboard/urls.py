from django.urls import path
from . import views

urlpatterns = [
    path('', views.leaderboards_view, name='leaderboard'),
]