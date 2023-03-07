from django.urls import path

from recipes.views import view_about, view_contact, view_home

urlpatterns = [
    path("", view_home),
    path("about/", view_about),
    path("contact/", view_contact),
]
