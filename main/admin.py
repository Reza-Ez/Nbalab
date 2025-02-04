from django.contrib import admin
from .models import *

class Profile(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone_number', 'age', 'bio')
    search_fields = ('user__username', 'name', 'bio')

admin.site.register(Profile_model, Profile)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author','body', 'title', 'time', 'image', 'is_hidden')
    search_fields = ('title', 'author__username')
    list_filter = ('is_hidden',)

admin.site.register(Article_model, ArticleAdmin)