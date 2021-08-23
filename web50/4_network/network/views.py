from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.http import JsonResponse
import json

from .models import User, Post, Follow, Likes
# https://docs.djangoproject.com/en/dev/topics/db/queries/
from django.db.models import F

PAGE_SIZE = 2

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


        # posts = [post.serialize() for post in posts]

        # p = Paginator(posts, PAGE_SIZE)
        # has_next = 


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




def profile(request, username):
    user = User.objects.get(username=username)

    # pagination and posts
    posts = Post.objects.filter(user=user).order_by("-timestamp").all()
    posts = [post.serialize() for post in posts]

    p = Paginator(posts, PAGE_SIZE)
    # has_next = 

    # check could be prolly broken with a user named AnonymousUser
    can_follow = not str(request.user) == username
    can_unfollow = bool(Follow.objects.filter(followed=User.objects.get(username=username)))

    # gets number of followers
    followers = Follow.objects.filter(followed=user).count()
    followed = Follow.objects.filter(follower=user).count()

    

    return render(request, "network/profile.html", {
        "user": user,
        "followed": followed,
        "followers": followers,
        "posts": posts,
        "can_follow": can_follow,
        "can_unfollow": can_unfollow
    })


@login_required(redirect_field_name='login')
def post(request):
    if request.method == "POST":
        body = request.POST['body']
        user = request.user
        Post(body=body, user=user).save()

        print(request.POST, request.user)
        return HttpResponseRedirect(reverse("index"))

    return HttpResponseRedirect(reverse("index"))


@login_required(redirect_field_name='login')
def following(request):
    if request.method == "POST":
        follower = request.user
        to_be_followed = User.objects.get(username=request.POST['followed'])

        already_followed = bool(Follow.objects.filter(followed=to_be_followed))
        for thing in request:
            print(thing)

        if to_be_followed and not already_followed:
            Follow(followed=to_be_followed, follower=follower).save()
        elif to_be_followed and already_followed:
            Follow.objects.filter(followed=to_be_followed).delete()
        else:
            # TODO return error
            pass

        return HttpResponseRedirect(reverse("index"))

    
    user = request.user

    # getting the posts of the followed people
    followed = Follow.objects.filter(follower=user)
    posts = []

    # TODO: make tests for this
    for person_followed_key in followed.iterator():
        this_posts = Post.objects.filter(user=person_followed_key.followed)
        posts += [post.serialize() for post in this_posts]

    return render(request, "network/following.html", {
        "posts": posts
    })

# IMPORTANT FIELDS IN REQUEST:
# Author, followers, all

def get_posts(request):

    if request.method != "POST":
        return JsonResponse({
                "error": "Only Post request supported."
            }, status=400)

    body = json.loads(request.body)
    active_states = 0

    # using binary coding to store the codes
    if 'author' in body:
        active_states += 1
    if 'following' in body:
        active_states += 2
    if 'all' in body:
        active_states += 4

    if active_states not in [1, 2, 4]:
        return JsonResponse({
            "error": "Can only use one active state"
        }, status=400)
    elif active_states == 0:
        return JsonResponse({
            "error": "Should select a correct state"
        }, status=400)

    if active_states == 1:
        user = User.objects.get(username=body['author'])

        # pagination and posts
        posts = Post.objects.filter(user=user).order_by("-timestamp").all()
        pages = Paginator(posts, PAGE_SIZE)

        current_page_number = body['page'] if 'page' in body  else 1
        current_page = pages.page(current_page_number)

        return JsonResponse({
            "posts": [post.serialize() for post in current_page],
            "has_next": current_page.has_next(),
            "has_previous": current_page.has_previous(),
            "total_pages": pages.num_pages
        })

    if active_states == 2:
        user = request.user

        # getting the posts of the followed people
        followed = [element.followed for element in Follow.objects.filter(follower=user)]
        posts = Post.objects.filter(user__in=followed)

        pages = Paginator(posts, PAGE_SIZE)

        current_page_number = body['page'] if 'page' in body  else 1
        current_page = pages.page(current_page_number)

        return JsonResponse({
            "posts": [post.serialize() for post in current_page],
            "has_next": current_page.has_next(),
            "has_previous": current_page.has_previous(),
            "total_pages": pages.num_pages
        })

    if active_states == 4:
        posts = Post.objects.all()
        pages = Paginator(posts, PAGE_SIZE)

        current_page_number = body['page'] if 'page' in body  else 1
        current_page = pages.page(current_page_number)
        return JsonResponse({
            "posts": [post.serialize() for post in current_page],
            "has_next": current_page.has_next(),
            "has_previous": current_page.has_previous(),
            "total_pages": pages.num_pages
        })


@login_required(redirect_field_name='login')
def like(request):
    if request.method != "POST":
        return JsonResponse({
                "error": "Only Post request supported."
            }, status=400)

    body = json.loads(request.body)
    user = request.user

    if not 'post' in body:
        return JsonResponse({
            "error": "couldn't find post id"
        }, status=400)

    post = Post.objects.get(pk=body['post'])

    if Likes.objects.filter(post):
        pass