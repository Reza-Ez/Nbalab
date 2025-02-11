from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE


class Profile_model(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    age = models.IntegerField(blank=True, null= True)
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True, null=True)

    def __str__(self):
        return self.user.username

    @staticmethod
    def get_or_create_profile(user):
        profile, created = Profile_model.objects.get_or_create(user=user)
        return profile

class Article_model(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False)
    like = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_by', blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Bookmark_model(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    article = models.ForeignKey(Article_model, on_delete = models.CASCADE)

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} saved {self.article.title}"


class Comment_model(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    article = models.ForeignKey('Article_model', on_delete = models.CASCADE, related_name='comments')
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete = models.CASCADE, null=True,blank=True, related_name='replies')

    def __str__(self):
        return f"{self.user.username} - {self.comment[:30]}"