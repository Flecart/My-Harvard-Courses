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
        return render(request, "pages/error.html")

    return render(request, "pages/page.html", {
        "title": title,
        "entry": entry
    })


def search(request):

    if request.method == "POST":
        query = request.POST["q"]
        search_answer = util.check_matches(query)

        if not search_answer.exactMatch:
            return render(request, "pages/search.html", {
                "query": query,
                "entries": search_answer.answers
            })
        return HttpResponseRedirect("wiki/" + search_answer.answers[0])

    else:
        return render(request, "pages/search.html", {
                "query": "Empty",
                "entries": []
            })


def new_page(request):

    if request.method == "POST":
        print(request.POST)
        trimmed = {
            'title': request.POST['title'].strip(),
            'body': request.POST['body'].strip()
        }

        form = util.new_page_form(trimmed)
        if form.is_valid():
            print(form)
        else:
            print("no")
        # search_answer = util.check_matches(title)
        pass
    
    else:
        return render(request, "pages/new_page.html", {
            "form": util.new_page_form()
        }) 