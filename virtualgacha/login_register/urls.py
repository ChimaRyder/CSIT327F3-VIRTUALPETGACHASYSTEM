from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingpage_view, name='landingpage'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
]
