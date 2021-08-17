from auctions.globals import MAX_LISTING_LEN
from django import forms

class ListingForm(forms.Form):

    title = forms.CharField(
        max_length=MAX_LISTING_LEN, 
        widget=forms.TextInput(attrs={
            "placeholder": "Listing Title"
        }))

    description = forms.CharField(
        max_length=MAX_LISTING_LEN, 
        widget=forms.TextInput(attrs={
            "placeholder": "Listing Description"
        }))

    starting_bid = forms.IntegerField(min_value=0, 
        required="Insert a valid number",
        widget=forms.TextInput(attrs={
            "placeholder": "Starting Bid"
        }))

    url = forms.CharField(
        required=False,
        max_length=MAX_LISTING_LEN, 
        widget=forms.TextInput(attrs={
            "placeholder": "Url to image (not required)"
        }))
        