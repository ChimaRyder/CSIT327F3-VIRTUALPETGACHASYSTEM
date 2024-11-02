from django.urls import path
from .views import *

urlpatterns = [
    path('', daily_rewards, name='daily_rewards'),
    path('claim/', claim_reward, name='claim_reward'),
]