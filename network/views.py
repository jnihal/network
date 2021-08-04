import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Profile, Post, Follower, Like

@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        creator = request.user
        content = request.POST["content"]

        post = Post(creator=creator, content=content)
        post.save()

        return HttpResponseRedirect(reverse("index"))
    
    posts = list(reversed(Post.objects.all()))
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print(page_obj[0].liked_users())

    return render(request, "network/index.html", {
        "posts": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"].title()
        last_name = request.POST["last_name"].title()
        profile_pic = request.FILES.get("profile_pic")

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            profile = Profile(user=user, profile_pic=profile_pic)
            user.save()
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url="login")
def profile(request, id):
    user = User.objects.get(pk=id)

    login_user = request.user

    following = Follower.objects.filter(follower=login_user, following=user).exists()

    return render(request, "network/profile.html", {
        "user": user,
        "posts": reversed(user.posts.all()),
        "followers_count": user.followers.count(),
        "following_count": user.following.count(),
        "post_count": user.posts.count(),
        "following": following
    })


@login_required(login_url="login")
def follow(request, user_id):
    if request.method == "POST":
        login_user = request.user
        user = User.objects.get(pk=user_id)
        
        following = Follower.objects.filter(follower=login_user, following=user).exists()

        if following:
            Follower.objects.filter(follower=login_user, following=user).delete()
            return JsonResponse({'status': 201, 'following': False, "follower_count": user.followers.count()}, status=201)
        
        else:
            follower = Follower(follower=login_user, following=user)
            follower.save()
            return JsonResponse({
                "status": 201,
                "following": True,
                "follower_count": user.followers.count()
            }, status=201)
    
    else:
        return JsonResponse({
            "error": "POST or PUT request required."
        }, status=400)


@login_required(login_url="login")
def following(request):
    if request.method == "POST":
        creator = request.user
        content = request.POST["content"]

        post = Post(creator=creator, content=content)
        post.save()

        return HttpResponseRedirect(reverse("index"))

    posts = []
    following = request.user.following.all()
    for profile in following:
        print(profile)
        posts.extend(profile.following.posts.all())
    
    posts.reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts": page_obj
    })


@login_required(login_url="login")
def like(request, post_id):
    if request.method == "POST":
        user = request.user
        post = Post.objects.get(pk=post_id)
        
        liked = Like.objects.filter(user=user, post=post).exists()

        if liked:
            Like.objects.filter(user=user, post=post).delete()
            return JsonResponse({'status': 201, 'liked': False, "like_count": post.likes.count()}, status=201)
        
        else:
            like = Like(user=user, post=post)
            like.save()
            return JsonResponse({
                "status": 201,
                "liked": True,
                "like_count": post.likes.count()
            }, status=201)
    
    else:
        return JsonResponse({
            "error": "POST or PUT request required."
        }, status=400)


@login_required(login_url="login")
def edit(request, post_id):
    if request.method == "POST":

        data = json.loads(request.body)

        content = data.get("content", "")

        post = Post.objects.get(pk=post_id)
        post.content = content
        post.save()

        return JsonResponse({"message": "Post edited successfully."}, status=201)
    
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)