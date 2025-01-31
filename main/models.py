from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import User

class EditProfile_model(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    age = models.IntegerField(blank=True, null= True)

    def __str__(self):
        return self.user.username
    @staticmethod
    def get_or_create_profile(user):
        profile, created = EditProfile_model.objects.get_or_create(user=user)
        return profile
