from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_profile, name='profile'),
    path('edit-profile/', views.edit_profile, name="edit_profile"),
    path('delete-account/', views.delete_account, name="delete_account"),
    path('showcase-pet/', views.showcase_pet, name="showcase_pet"),
    path('update-showcase/', views.update_showcase, name='update_showcase'),
]