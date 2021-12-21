from django.shortcuts import render
import markdown2
from django import forms
from . import util
import random


class ExistingForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        entries = util.list_entries()
        for i in range(len(entries)):
            if title.upper() == entries[i].upper():
                raise forms.ValidationError('that title already exists')
        return title


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html")

    else:
        return render(request, "encyclopedia/entry.html", {
            "content": markdown2.markdown(util.get_entry(title)),
            "title": title
        })

def search(request):
    if request.method == "POST":
        item = request.POST.get('searched').capitalize()

    entries = util.list_entries()
    close = []

    for i in range(len(entries)):
        if item.capitalize() == entries[i].capitalize():
            return entry(request, item)
        elif item.upper() in entries[i].upper():
            close.append(entries[i])

    if len(close) != 0:
        return render(request, "encyclopedia/search.html", {
            "entries": close
        })
    else:
        return render(request, "encyclopedia/error.html")

def add(request):

    if request.method=="POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            newtitle = form.cleaned_data["title"]
            newcontent = form.cleaned_data["content"]

            util.save_entry(newtitle,newcontent)
            return entry(request, newtitle)
        else:
            return render(request, "encyclopedia/add page.html", {
                "form": form
            })

    return render(request, "encyclopedia/add page.html", {
        "form": NewEntryForm()
        })

def edit(request, title):
    if request.method=="POST":
        form = ExistingForm(request.POST)
        if form.is_valid():
            newtitle = form.cleaned_data["title"]
            newcontent = form.cleaned_data["content"]

            util.save_entry(newtitle,newcontent)
            return entry(request, newtitle)
        else:
            return render(request, "encyclopedia/edit page.html", {
                "form": form
            })

    content = util.get_entry(title)
    data= {
        'title': title,
        'content': content
    }
    form=ExistingForm(data)
    return render(request, "encyclopedia/edit.html", {
        "form": form
        })

def edit2(request):
    if request.method=="POST":
        form = ExistingForm(request.POST)
        if form.is_valid():
            newtitle = form.cleaned_data["title"]
            newcontent = form.cleaned_data["content"]

            util.save_entry(newtitle,newcontent)
            return entry(request, newtitle)
        else:
            return render(request, "encyclopedia/edit page.html", {
                "form": form
            })

def rnm(request):
    entries = util.list_entries()
    x = random.randint(0, len(entries)-1)
    title=entries[x]


    return entry(request, title)










