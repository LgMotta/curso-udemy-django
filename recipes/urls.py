from django.urls import path

from recipes.views import view_about, view_home

urlpatterns = [path("", view_home), path("about/", view_about)]
