"""
URL configuration for nbalab project.

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
from django.contrib import admin
from django.urls import path,include
from main import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('Register/', views.register_view, name='register'),
    path('Login/', views.login_view, name='login'),
    path('Logout/', views.logout_view, name='logout'),
    path('Profile/', views.profile_view, name='profile'),
    path('Edit_Profile/', views.edit_profile_view, name='Edit_Profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)