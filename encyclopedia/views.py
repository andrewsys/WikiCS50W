from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from markdown2 import Markdown
from random import randint
from . import util

class SearchForm(forms.Form):
    wikisearch = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    nptitle = forms.CharField(label="Title")
    npcontent = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Markdown content', 'style': 'height: 80vh;'}))


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
    markdowner = Markdown()
    wikicontent = markdowner.convert(util.get_entry(wikititle))

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
            return wikipage(request, nptitle)

    return render(request, "encyclopedia/newpage.html", {
        "cform": NewPageForm(),
        "form": SearchForm()
    })

def modify(request):
    if request.method == 'POST':
        mtitle = request.POST.get('mtitle', None)
        if not mtitle == None:
            for title in util.list_entries():
                if mtitle == title:
                    mcontent = util.get_entry(mtitle)
                    return render(request, "encyclopedia/modify.html", {        
                        "form": SearchForm(),
                        "title": mtitle,
                        "content": mcontent,
                    })
        else:
            emtitle = request.POST.get('emtitle', None)
            for title in util.list_entries():
                if emtitle == title:
                    emcontent = request.POST.get('emcontent', None)
                    file = open(f"entries/{emtitle}.md", 'w')
                    file.write(emcontent)
                    file.close()
                    return wikipage(request, emtitle)
    return index(request)

def randpage(request):
    pages = util.list_entries()
    goto = randint(0, len(pages))-1

    return wikipage(request, pages[goto])