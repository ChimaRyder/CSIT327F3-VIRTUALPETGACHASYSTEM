from django.urls import path
from .views import base, terms_of_service

urlpatterns = [
    path('', base, name='base'),
    path('terms-of-service', terms_of_service, name='terms-of-service'),
]