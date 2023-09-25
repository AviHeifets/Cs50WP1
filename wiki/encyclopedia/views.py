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


def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        entries = util.list_entries()

        if not form.is_valid():
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "form": form
            })

        if form.cleaned_data['q'] in entries:
            return HttpResponseRedirect(f"wiki/{form.cleaned_data['q']}")

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def show_entry(request, title):
    found_entry = util.get_entry(title)
    if found_entry is None:
        return render(request, "encyclopedia/error_not_found.html", {
            "TITLE": title.upper()
        })

    return render(request, "encyclopedia/entry_page.html", {
        "TITLE": title,
        "entry": found_entry
    })
