from django.contrib import admin
from .models import *

class Profile(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone_number', 'age', 'bio')
    search_fields = ('user__username', 'name', 'bio')

admin.site.register(Profile_model, Profile)
# Register your models here.
