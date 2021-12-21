from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="searched"),
    path("add", views.add, name="add"),
    path("edit2", views.edit2, name="edit2"),
    path("rnm", views.rnm, name="rnm"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("<str:title>", views.entry, name="entry"),
    path("error", views.entry, name="error"),

]
