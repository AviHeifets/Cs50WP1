from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
