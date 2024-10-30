from django.urls import path
from .views import chat_view, message_list

urlpatterns = [
    path('', chat_view, name="chat_view"),
    path('api/messages/global/', message_list, name='global_message_list'),
]