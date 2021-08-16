from django.http.request import RAISE_ERROR
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):

    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/error.html")

    return render(request, "encyclopedia/page.html", {
        "title": title,
        "entry": entry
    })



def wiki_redirect(request):
    return HttpResponseRedirect(reverse('index'))

    
def search(request):

    if request.method == "POST":
        query = request.POST["q"]
        search_answer = util.check_matches(query)

        if not search_answer.exactMatch:
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "entries": search_answer.answers
            })
        return HttpResponseRedirect(reverse('wiki') + search_answer.answers[0])

    else:
        return render(request, "encyclopedia/search.html", {
                "query": "Empty",
                "entries": []
            })


def new_page(request):

    if request.method == "POST":
        
        form = util.entry_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            if util.check_matches(title).exactMatch:
                error_message = "There is a entry with the same title (this app is case insensitive)"
                code = 409

                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "code": code,
                    "message": error_message
                })

            util.save_entry(title, content)

            return HttpResponseRedirect(reverse('wiki') + '/' + title)
        else:
            error_message = "Input is not valid"
            code = 400

            return render(request, "encyclopedia/new_page.html", {
                "form": form,
                "code": code,
                "message": error_message
            })
    
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": util.entry_form(),
            "code": 200,
            "message": ""
        }) 


def edit_page(request):
    if request.method == "POST":
        form = util.entry_form(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            if not util.check_matches(title).exactMatch:
                error_message = "Don't try to hack me! This page does not exist!"
                code = 400

                return render(request, "encyclopedia/edit_page.html", {
                    "form": form,
                    "code": code,
                    "message": error_message
                })

            util.save_entry(title, content)

            return HttpResponseRedirect(reverse('wiki') + '/' + title)
        else:
            error_message = "Input is not valid"
            code = 400

            return render(request, "encyclopedia/edit_page.html", {
                "form": form,
                "code": code,
                "message": error_message
            })

    form = util.entry_form(request.GET)

    return render(request, "encyclopedia/edit_page.html", {
        "form": form,
        "code": 200,
        "message": ""
    })


def random_page(request):
    page = util.get_random_page()
    return HttpResponseRedirect(reverse('wiki') + '/' + page)
