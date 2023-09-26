from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.show_entry, name="show_entry"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("edit_entry/<str:title>", views.edit_entry, name="edit_entry")
]
