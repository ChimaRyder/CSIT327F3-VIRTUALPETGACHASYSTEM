from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.user_profile, name='profile'),
    path('<str:username>/', views.user_profile, name='other_profile'),
    path('/edit-profile/', views.edit_profile, name='edit_profile'),
    path('/delete-account/', views.delete_account, name="delete_account"),
    path('showcase_pet/<int:pet_id>/', views.showcase_pet, name='showcase_pet'),
    path('unshowcase_pet/<int:pet_id>/', views.unshowcase_pet, name='unshowcase_pet'),
    # path('achievements/', views.achievements, name="achievements")
]