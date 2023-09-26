from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util


class SearchForm(forms.Form):
    q = forms.CharField(
        label='',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'search', 'placeholder': 'Search Encyclopedia'})
    )


class NewEntryForm(forms.Form):
    name = forms.CharField(
        label='name',
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'name'}),
    )
    data = forms.CharField(
        label='Entry',
        widget=forms.Textarea(attrs={'placeholder': 'Data'})
    )

class EditForm(forms.Form):
    data = forms.CharField(
        label='Entry',
        widget=forms.Textarea(attrs={'placeholder': 'Data'})
    )


def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        entries = util.list_entries()

        if not form.is_valid():
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "form": form,
                "header": "All Pages"
            })

        cleaned = form.cleaned_data['q'].upper()

        if cleaned in entries:
            return HttpResponseRedirect(f"wiki/{cleaned}")

        # find all results that are substrings
        substrings = filter(lambda x: (cleaned in x), entries)
        return render(request, "encyclopedia/index.html", {
            "entries": substrings,
            "form": form,
            "header": "Similar Results"
        })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm(),
        "header": "All Pages"
    })


def show_entry(request, title):
    found_entry = util.get_entry(title)

    if found_entry is None:
        return render(request, "encyclopedia/error.html", {
            "TITLE": title.upper(),
            "massage": "Not found!"
        })

    return render(request, "encyclopedia/entry_page.html", {
        "title": title,
        "entry": found_entry
    })


def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if not form.is_valid():
            return render(request, "encyclopedia/new_entry.html", {
                'form': NewEntryForm()
            })

        if form.cleaned_data['name'].upper() in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "TITLE": '',
                "massage": "Entry already exists!"
            })

        util.save_entry(form.cleaned_data['name'].upper(), form.cleaned_data['data'])
        return HttpResponseRedirect(f"wiki/{form.cleaned_data['name'].upper()}")

    return render(request, "encyclopedia/new_entry.html", {
        'form': NewEntryForm()
    })


def edit_entry(request, title):
    data = util.get_entry(title)
    form = EditForm(initial={'data': data})
    title = title

    if request.method == "POST":
        form = EditForm(request.POST)

        if not form.is_valid():
            form = EditForm(initial={'data': data})
            return render(request, "encyclopedia/new_entry.html", {
                'form': form,
                'title': title
            })

        util.save_entry(title, form.cleaned_data['data'])
        return HttpResponseRedirect(reverse("encyclopedia:show_entry", args=[title]))

    return render(request, "encyclopedia/edit_entry.html", {
        'form': form,
        'title': title
    })
