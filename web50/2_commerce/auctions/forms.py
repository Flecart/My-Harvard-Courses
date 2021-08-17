from django.forms import widgets
from auctions.globals import MAX_LISTING_LEN, MAX_DESCRIPTION_LEN

from django import forms
from . import util

class ListingForm(forms.Form):

    def __init__(self, choices_list, *args, **kwargs):   
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['categories'].choices = choices_list

    title = forms.CharField(
        max_length=MAX_LISTING_LEN, 
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Listing Title"
        }))

    description = forms.CharField(
        max_length=MAX_DESCRIPTION_LEN, 
        widget=forms.Textarea(attrs={
            "rows": 3,
            "class": "form-control",
            "placeholder": "Listing Description"
        }))

    starting_bid = forms.IntegerField(min_value=0, 
        required="Insert a valid number",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Starting Bid"
        }))

    url = forms.CharField(
        required=False,
        max_length=MAX_DESCRIPTION_LEN, 
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Url to image (not required)"
        }))

    categories = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
    )


class BidForm(forms.Form):
    bid = forms.IntegerField(
        label=False,
        widget=forms.TextInput(attrs={
            "placeholder": "E.G: 1",
            "class": "form-control",
            "aria-label": "Bid Amount (to the nearest dollar)"
        }))

    listing_id = forms.CharField(
        max_length=MAX_LISTING_LEN,
        widget=forms.HiddenInput
    )

class CommentForm(forms.Form):
    content = forms.CharField(
        max_length=MAX_DESCRIPTION_LEN,
        label=False,
        widget=forms.TextInput(attrs={
            "class": "form-control mb-3",
            "placeholder": "Comment"
        }))
    