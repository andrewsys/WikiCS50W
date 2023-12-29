from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from . import util

class SearchForm(forms.Form):
    wikisearch = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    nptitle = forms.CharField(label="Title")
    npcontent = forms.CharField(label="Content", widget=forms.Textarea(attrs={'style': 'height: 80vh;'}))


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

            if not foundtitles:
                foundtitles.append("No pages were found")

            return render(request, "encyclopedia/search.html", {
                "wikisearch": wikisearch,
                "foundtitles": foundtitles,
                "form": SearchForm()
            })
        else:
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": SearchForm()
        })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def wikipage(request, wikititle):
    wikicontent = util.get_entry(wikititle)

    return render(request, "encyclopedia/wikipage.html", {
        "wikititle": wikititle,
        "wikicontent": wikicontent,
        "form": SearchForm(),
    })

def newpage(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        wikititles = util.list_entries()

        if form.is_valid():
            nptitle = form.cleaned_data["nptitle"]
            npcontent = form.cleaned_data["npcontent"]

            for titles in wikititles:
                if titles == nptitle:
                    return HttpResponse("Error: Page already exists.")

            file = open(f"entries/{nptitle}.md", 'w')
            file.write(npcontent)
            file.close()
            return index(request)

    return render(request, "encyclopedia/newpage.html", {
        "cform": NewPageForm(),
        "form": SearchForm()
    })