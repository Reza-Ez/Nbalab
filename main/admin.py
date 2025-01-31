from django.contrib import admin
from .models import *

class EditProfile(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone_number', 'age', 'bio')
    search_fields = ('user__username', 'name', 'bio')

admin.site.register(EditProfile_model, EditProfile)
# Register your models here.
