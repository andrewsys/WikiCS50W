from django.shortcuts import render
from django import forms
from django.http import HttpResponse

from . import util

class SearchForm(forms.Form):
    wikisearch = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))


def index(request):
    foundtitles = []
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            wikisearch = form.cleaned_data["wikisearch"]

            for title in util.list_entries():
                if wikisearch.upper() == title.upper():
                    return wikipage(request, title)
                if title.upper().find(wikisearch.upper()) != -1:
                    foundtitles.append(title)

            print(foundtitles)

            if not foundtitles:
                foundtitles.append("No pages were found")

            return render(request, "encyclopedia/search.html", {
                "wikisearch": wikisearch,
                "foundtitles": foundtitles,
                "form": SearchForm()
            })
        else:
            return HttpResponse("Invalid")


    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def wikipage(request, wikititle):
    wikicontent = util.get_entry(wikititle)

    return render(request, "encyclopedia/wikipage.html", {
        "wikititle": wikititle,
        "wikicontent": wikicontent,
        "form": SearchForm()
    })