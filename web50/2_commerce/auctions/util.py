import requests
from .models import Bid, Category, User, Listing, Watchlist, Comment
from . import validators
from django.core.exceptions import ObjectDoesNotExist


def save_listing(form, user_id) -> None:
    title = form.cleaned_data['title']
    description = form.cleaned_data['description']
    starting_bid = form.cleaned_data['starting_bid']
    url = validators.url_cleaner(form.cleaned_data['url'])
    user = User.objects.get(pk=user_id)

    Listing(author=user, title=title, description=description, current_bid=starting_bid, image_link=url).save()


def is_url_image(image_url):
    """
    Checks if the url in input is an image, returns boolean
    see here https://stackoverflow.com/questions/10543940/check-if-a-url-to-an-image-is-up-and-exists-in-python
    """
    image_formats = ("image/png", "image/jpeg", "image/jpg", "image/gif")
    r = requests.head(image_url)
    if r.headers["content-type"] in image_formats:
        return True
    return False


def find_bidder(queryset):
    if not queryset:
        return "No_bidder"

    # TODO: test if this is the name of the bidder, and if this is the name of the highest bidder
    return queryset[0]


def add_bidders(queryset, is_single=False):
    """
    Dinamic function to add bidder to the querysets for listeners
    """
    if is_single:
        queryset.bidder = find_bidder(Bid.objects.filter(listing=queryset).order_by("-highest_bid"))
        return queryset

    for listing in queryset:
        listing.bidder = find_bidder(Bid.objects.filter(listing=listing).order_by("-highest_bid"))

    return queryset


def create_listing(user_id=0, only_watchlist=False, only_active=False):
    """
    only_active gets only the opened listings
    only_watchlist gives the list of Listings in watchlist
    if these two are false gives every listing
    """
    if only_active:
        return add_bidders(Listing.objects.filter(closed=False))

    if not only_watchlist:
        listings = add_bidders(Listing.objects.all())
        return listings

    else:
        user = User.objects.get(pk=user_id)
        listings_id = []
        for watchlist in Watchlist.objects.filter(user=user):
            listings_id.append(watchlist.listing.id)
        listings = add_bidders(Listing.objects.filter(pk__in=listings_id))
        return listings


def is_on_watchlist(user_id, listing_id) -> bool:
    listing = Listing.objects.get(pk=listing_id)
    listing_watchlist = Watchlist.objects.filter(listing=listing)
    user = User.objects.get(pk=user_id)

    for item in listing_watchlist:
        if item.user == user:
            return True

    return False


def save_watchlist(user_id, listing_id) -> None:
    user = User.objects.get(pk=user_id)
    listing = Listing.objects.get(pk=listing_id)

    try:
        Watchlist.objects.get(user=user, listing=listing).delete()
    except ObjectDoesNotExist:
        Watchlist(user=user, listing=listing).save()


def is_valid_bid(form) -> True:
    bid = form.cleaned_data['bid']
    listing_id = form.cleaned_data['listing_id']

    # https://stackoverflow.com/questions/51905712/how-to-get-the-value-of-a-django-model-field-object
    listing = Listing.objects.get(pk=listing_id)
    current_bid = getattr(listing, "current_bid")

    if bid <= current_bid:
        return False
    
    return True


def save_bid(form, user_id):
    bid = form.cleaned_data['bid']
    user = User.objects.get(pk=user_id)
    listing_id = form.cleaned_data['listing_id']
    listing = Listing.objects.get(pk=listing_id)
    listing.current_bid = bid
    listing.save()

    Bid(listing=listing, current_bidder=user, highest_bid=bid).save()
    

def extract_id_from_url(url):
    """
    finds the listing id of the listing from the requesting page
    extracts from the url
    """
    splitted = url.split("/")
    index = splitted.index('listing') + 1
    id_and_get = splitted[index]

    try:
        get_param_index = id_and_get.index('?')
        return id_and_get[0:get_param_index]

    except ValueError:
        return id_and_get


def save_closing_listing(user_id, listing_id):
    user = User.objects.get(pk=user_id)
    listing = Listing.objects.get(pk=listing_id)
    author = getattr(listing, "author")

    if user != author:
        return False

    listing.closed = True
    listing.save()
    return True


def get_listing_winner(listing) -> int:
    bids = Bid.objects.filter(listing=listing).order_by("-highest_bid")
    try:
        winner_id = bids[0].current_bidder.id
    except IndexError:
        # meaning that probably a listening closed with no bidders
        return False
    return winner_id


def get_comments(listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return Comment.objects.filter(listing=listing)


def save_comment(form, listing_id, user_id):
    content = form.cleaned_data['content']
    user = User.objects.get(pk=user_id)
    listing = Listing.objects.get(pk=listing_id)
    Comment(author=user, listing=listing, content=content).save()


def get_categories():
    all_list = Category.objects.all()
    list_names = []
    for category in all_list:
        list_names.append((category.name, category.name))

    return list_names