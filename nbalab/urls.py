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
    path('Articles', views.articles_view, name='articles'),
    path('My_Articles', views.my_articles_view, name='my_articles'),
    path('New_Article', views.new_article_view, name='new_article'),
    path('Edit_Article/<str:title>',views.edit_article_view, name='edit_article' ),
    path('Delete_Article/<str:title>',views.delete_article_view, name='delete_article' ),
    path('Hide_Article/<str:title>',views.hide_article_view, name='hide_article' ),
    path('Show_Article/<str:title>',views.show_article_view, name='show_article' ),
    path('Articles/<str:title>/',views.article_url_view, name='article_url'),
    path('Search/', views.search_view, name='search'),
    path('like/<int:article_id>',views.like_view, name='likes'),
    path('Bookmarks/', views.bookmark_view, name='bookmark'),
    path('save_article/<int:article_id>/', views.toggle_bookmark_view, name='save_article'),
    path('article/<int:article_id>/add_comment/', views.add_comment_view, name='add_comment'),
    path('article/<int:article_id>/comment/<int:comment_id>/delete/', views.delete_comment_view, name='delete_comment'),
    path('profile/<str:username>/', views.public_profile_view, name='public_profile'),
    path('follow/<str:username>/', views.follow_view, name='follow'),
]

urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)