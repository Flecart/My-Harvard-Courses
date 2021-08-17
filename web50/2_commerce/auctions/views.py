from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listing, Comment, Bid, Watchlist
from . import util

def index(request):

    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        listings = Listing.objects.filter(author=user)
        return render(request, "auctions/index.html", {
            "listings": listings
        })

    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            user_id = User.objects.get(username=username).id
            request.session['user_id'] = user_id
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(redirect_field_name='login')
def create_listing(request):
    if request.method == "POST":
        form = util.ListingForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            url = form.cleaned_data['url'] 
            user = User.objects.get(id=request.session['user_id'])

            listing = Listing(author=user, title=title, description=description, current_bid=starting_bid, image_link=url)
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form,
                "message": "Invalid Input"
            })
    
    return render(request, "auctions/create_listing.html", {
        "form": util.ListingForm(),

    })


@login_required(redirect_field_name='login')
def watchlist(request):
    user = User.objects.get(id=request.session['user_id'])
    listings_id = Watchlist.objects.filter(user=user)
    listings = Listing.objects.filter(pk__in=listings_id)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def listing(request):
    listings = Listing.objects.all()
    return render(request, "auctions/listing.html", {
        "listings": listings
    })


def listing_page(request, id):  
    try:
        listing = Listing.objects.get(pk=id)

        return render(request, "auctions/listing_page.html", {
            "listing": listing
        })
    except ObjectDoesNotExist:
        return render(request, "auctions/404.html")