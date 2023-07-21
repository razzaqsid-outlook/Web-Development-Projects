from django.urls import path

from . import views
import encyclopedia

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("Search_Results", views.search_bar, name="search_bar"),
    path("<name>", views.title, name="title"),
    path("Entries/New", views.New_Entry, name="new_entry"),
    path("<name>/edit", views.Edit_Entry, name="edit_entry"),
    path("Entries/Random", views.Random_Entry, name="random_entry"),
]
