from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Post, Follow


def index(request):
    posts = Post.objects.all()
    return render(request, "network/index.html", {
        "posts": [post.serialize() for post in posts]
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
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(redirect_field_name='login')
def post(request):
    if request.method == "POST":
        body = request.POST['body']
        user = request.user
        Post(body=body, user=user).save()

        print(request.POST, request.user)
        return HttpResponseRedirect(reverse("index"))

    return HttpResponseRedirect(reverse("index"))


def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user).order_by("-timestamp").all()

    # check could be prolly broken with a user named AnonymousUser
    can_follow = not str(request.user) == username
    
    followed = Follow.objects.filter(followed=user).count()
    followers = Follow.objects.filter(follower=user).count()

    return render(request, "network/profile.html", {
        "user": user,
        "followed": followed,
        "followers": followers,
        "posts": [post.serialize() for post in posts],
        "can_follow": can_follow
    })

