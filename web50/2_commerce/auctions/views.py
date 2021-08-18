from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listing, Comment, Bid, Watchlist
from . import util
from . import forms

def index(request):
    listings = util.create_listing(only_active=True)

    return render(request, "auctions/index.html", {
        "listings": listings
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


def listing(request):
    listings = util.create_listing(only_watchlist=False)

    return render(request, "auctions/listing.html", {
        "listings": listings
    })


def listing_page(request, listing_id):  
    try:
        listing = util.add_bidders(Listing.objects.get(pk=listing_id), is_single=True)
    except ObjectDoesNotExist:
        return render(request, "auctions/404.html")
    
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        user_id = 1 # should use standard nobody id here instead

    if listing.closed and util.get_listing_winner(listing) == user_id:
        message = "Congratulations! You won this bid!"
    else:
        message = False
    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "is_on_watchlist": util.is_on_watchlist(user_id, listing_id),
        "bid_form": forms.BidForm(initial={"listing_id": listing_id}),
        "success_message": request.GET.get("success_message", message),
        "error_message": request.GET.get("error_message", False),
        "comment_form": forms.CommentForm(),
        "comments": util.get_comments(listing_id),
    })


@login_required(redirect_field_name='login')
def create_listing(request):
    if request.method == "POST":
        print(request.POST)
        form = forms.ListingForm(request.POST, categories_list=util.get_categories())
        print(form)

        if form.is_valid():
            util.save_listing(form, request.session['user_id'])
            return HttpResponseRedirect(reverse('index'))
        else:
            # print(form)
            return render(request, "auctions/create_listing.html", {
                "form": form,
                "message": "Invalid Input"
            })
    
    return render(request, "auctions/create_listing.html", {
        "form": forms.ListingForm(categories_list=util.get_categories()),
    })


@login_required(redirect_field_name='login')
def watchlist(request):
    if request.method == "POST":

        bid = util.extract_id_from_url(request.META.get('HTTP_REFERER'))
        if "id" in request.POST:
            bid = request.POST['id']
            util.save_watchlist(request.session['user_id'], bid)

            message = "Changed watchlist preferences successfully"
            return HttpResponseRedirect(reverse('listing') + f"/{bid}?success_message={message}")

        message = "Error in changing watchlist preferences"
        return HttpResponseRedirect(reverse('listing') + f"/{bid}?error_message={message}")
        
    # dont need to check if user_id is present bc its @login_required
    listings = util.create_listing(user_id=request.session['user_id'], only_watchlist=True)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required(redirect_field_name='login')
def bid(request):
    if request.method == "POST":
        form = forms.BidForm(request.POST)
        listing_id = util.extract_id_from_url(request.META.get('HTTP_REFERER'))

        if form.is_valid() and util.is_valid_bid(form):
            util.save_bid(form, request.session['user_id'])

            message = "Bid saved successfully"
            return HttpResponseRedirect(reverse('listing') + f"/{listing_id}?success_message={message}")
        
        else:
            message = "Invalid Bid Input, check bid value, or bid closed"
            return HttpResponseRedirect(reverse('listing') + f"/{listing_id}?error_message={message}")

    return HttpResponseRedirect(reverse('index'))


@login_required(redirect_field_name='login')
def close(request):
    if request.method == "POST":
        listing_id = util.extract_id_from_url(request.META.get('HTTP_REFERER'))
        success = util.save_closing_listing(request.session['user_id'], listing_id)

        if success:
            message = "Listing closed successfully"
            return HttpResponseRedirect(reverse('listing') + f"/{listing_id}?success_message={message}")

        message = "You cannot closed listing of others"
        return HttpResponseRedirect(reverse('listing') + f"/{listing_id}?error_message={message}")
    
    return HttpResponseRedirect(reverse('index'))


@login_required(redirect_field_name='login')
def comment(request):
    if request.method == "POST":
        listing_id = util.extract_id_from_url(request.META.get('HTTP_REFERER'))
        form = forms.CommentForm(request.POST)

        if form.is_valid():
            try:
                util.save_comment(form, listing_id, request.session['user_id'])
            except:
                message = "Errors in saving the comment"
                return HttpResponseRedirect(reverse('listing') + f"/{listing_id}?error_message={message}")

            message = "Comment saved successfully"
            return HttpResponseRedirect(reverse('listing') + f"/{listing_id}?success_message={message}")

        message = "Invalid Comment"
        return HttpResponseRedirect(reverse('listing') + f"/{listing_id}?error_message={message}")
    
    return HttpResponseRedirect(reverse('index'))


def category(request):
    categories = [item[0] for item in util.get_categories()]

    return render(request, "auctions/category.html", {
        "categories": categories
    })


def category_name(request, category_name):
    listings = util.create_listing(category=category_name)
    print(listings)
    return render(request, "auctions/category_page.html", {
        "listings": listings
    })