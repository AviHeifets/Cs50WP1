from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def show_entry(request, TITLE):
    found_entry = util.get_entry(TITLE)
    if found_entry is None:
        return render(request, "encyclopedia/error_not_found.html", {
            "TITLE": TITLE.upper()
        })

    return render(request, "encyclopedia/error_not_found.html", {
        "TITLE": TITLE
    })
