"""
URL configuration for virtualgacha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from inspect import stack

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from virtualgacha import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(next_page='landingpage'), name='logout'),
    path('base/', include('base_template.urls')),
    path('', include('login_register.urls')),
    path('lootbox/', include('lootbox_market.urls')),
    path('my_pets/', include('inventory.urls')),
    path('adventure/', include('adventure.urls')),
    path('market/', include('marketplace.urls')),
    path('chat/', include('chat.urls')),
    path('profile/', include('user_profile.urls')),
    path('daily/', include('daily_rewards.urls')),
    path('checkout/', include('checkout_system.urls')),
    path('notifications/', include('notification.urls')),
    path('staff/', include('admin_system.urls')),
    path('leaderboard/', include('leaderboard.urls')),
    path('trade/', include('trading.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
