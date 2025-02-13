from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import *
from .models import *
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages



def home_view(request):
    return render(request, 'base/home.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()

    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    form = LoginForm()
    error = ''

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username , password = password)

            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                error = "Username or password is incorrect"
    return render(request, 'authentication/login.html', {'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    profile, created = Profile_model.objects.get_or_create(user=request.user)
    return render(request, 'profile/profile.html', {'user': request.user,'profile': profile})


@login_required
def edit_profile_view(request):
    profile, created = Profile_model.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            profile.name = form.cleaned_data.get('name')
            profile.age = form.cleaned_data.get('age')
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.bio = form.cleaned_data.get('bio')
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            messages.success(request, "Profile updated successfully")
            return redirect('Edit_Profile')

    else:
        form = EditProfileForm(instance=request.user)

    form.fields['name'].initial = profile.name
    form.fields['age'].initial = profile.age
    form.fields['phone_number'].initial = profile.phone_number
    form.fields['bio'].initial = profile.bio

    return render(request, 'profile/editprofile.html', {'form': form, 'profile': profile})


def articles_view(request):
    sort_by = request.GET.get('sort','date')
    if sort_by == 'likes':
        articles = Article_model.objects.order_by('-like')
    elif sort_by == 'views':
        articles = Article_model.objects.order_by('-views')
    elif sort_by == 'alphabetical':
        articles = Article_model.objects.order_by('title')
    else :
        articles = Article_model.objects.order_by('-time')

    return render(request, 'articles/articles.html', {'articles': articles, 'sort_by': sort_by})


@login_required
def my_articles_view(request):
    my_articles = Article_model.objects.filter(author=request.user).order_by('-time')
    return render(request, 'articles/my_articles.html', {'articles': my_articles})


@login_required
def new_article_view(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Article created successfully")
            return redirect('my_articles')
    else:
        form = ArticleForm()
    return render(request, 'articles/new_article.html', {'form': form})


@login_required
def edit_article_view(request,title):
    article = get_object_or_404(Article_model,title=title)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('my_articles')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/edit_article.html', {'form': form, 'article': article})


@login_required
def delete_article_view(request,title):
    article = get_object_or_404(Article_model, title=title)
    article.delete()
    return redirect('my_articles')


@login_required
def hide_article_view(request,title):
    article = get_object_or_404(Article_model,title=title)
    article.is_hidden = True
    article.save()
    return redirect('my_articles')


@login_required
def show_article_view(request,title):
    article = get_object_or_404(Article_model,title=title)
    article.is_hidden = False
    article.save()
    return redirect('my_articles')


def article_url_view(request, title):
    article = get_object_or_404(Article_model,title=title)

    if request.user != article.author:
        article.views = article.views + 1
        article.save()

    comments = Comment_model.objects.filter(article=article, reply=None).order_by('-time')
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            reply_id = request.POST.get('reply_id')
            if reply_id:
                reply_comment = Comment_model.objects.get(id=reply_id)
                new_comment.reply = reply_comment
            new_comment.save()
            return redirect('article_url', title=article.title)

    return render(request, 'articles/article_url.html', {'article': article
        , 'comments': comments
        , 'form': form
            })


def search_view(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '').strip()
        if searched:
            articles = Article_model.objects.filter(title__icontains=searched)
        else:
            articles = []
        return render(request, 'base/search.html', {'articles': articles, 'searched': searched})
    return render(request, 'base/search.html', {'articles': [], 'searched': ''})


@csrf_exempt
@login_required
def like_view(request, article_id):
    if request.method == "POST":
        article = get_object_or_404(Article_model, id = article_id)
        if request.user in article.liked_by.all():
            article.liked_by.remove(request.user)
            liked = False
        else:
            article.liked_by.add(request.user)
            liked = True
        article.like =  article.liked_by.count()
        article.save()
        return JsonResponse({'liked': liked, "like_count": article.like})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def toggle_bookmark_view(request, article_id):
    article = get_object_or_404(Article_model, id=article_id)
    bookmark , created = Bookmark_model.objects.get_or_create(user = request.user, article = article)

    if not created:
        bookmark.delete()
        return JsonResponse({"bookmarked": False, "message": "Bookmark Removed!"})

    else :
        return JsonResponse({"bookmarked": True, "message": "Article Saved!"})


@login_required
def bookmark_view(request):
    bookmarks = Bookmark_model.objects.filter(user=request.user)
    saved_articles = [bookmark.article for bookmark in bookmarks]

    return render(request, 'articles/saved_articles.html', {'saved_articles': saved_articles})


@csrf_exempt
@login_required
def add_comment_view(request, article_id):
    if request.method == "POST":
        data = json.loads(request.body)
        reply_id = data.get('reply_id')
        article = get_object_or_404(Article_model, id=article_id)
        data = json.loads(request.body)
        comment = data.get("comment", "")
        reply_comment = None
        if reply_id:
            reply_comment = get_object_or_404(Comment_model, id=reply_id)
        if not comment:
            return JsonResponse({"success": False, "error": "Invalid input"} ,status=400)

        article = get_object_or_404(Article_model, id=article_id)
        comment = Comment_model.objects.create(user=request.user, article = article, comment=comment, reply=reply_comment)

    return JsonResponse({"success": True, 'comment_id': comment.id ,"comment": comment.comment,
                         "username": request.user.username, "time": comment.time.strftime('%b %d, %Y %H:%M'),
                         'reply_id': reply_id})

@login_required
def delete_comment_view(request, article_id, comment_id):
    article = get_object_or_404(Article_model, id=article_id)
    comment = get_object_or_404(Comment_model, id=comment_id, article_id=article_id)

    if request.user == comment.user:
        comment.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "You do not have permission to delete this comment"}, status=403)


def public_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    articles = Article_model.objects.filter(author=user)
    followed_users = Follow_model.objects.filter(follower=request.user).values_list('followed', flat=True)
    context = {
        'articles': articles,
        'profile_user': user,
        'followed_users': list(followed_users),
    }
    return render(request, 'profile/public_profile.html', context)


@login_required
def follow_view(request,username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user == user_to_follow:
        return JsonResponse({'error_message': "You Can't Follow Yourself"}, status=400)

    follow, created = Follow_model.objects.get_or_create(follower=request.user, followed=user_to_follow)

    if not created:
        follow.delete()
        followers_count = Follow_model.objects.filter(follower=user_to_follow).count()
        return JsonResponse({'followed':False, 'followers_count': followers_count})

    followers_count = user_to_follow.followers.count()
    return JsonResponse({'followed': created, 'followers_count': followers_count})
