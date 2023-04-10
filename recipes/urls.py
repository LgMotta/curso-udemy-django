from django.urls import path

from . import views

urlpatterns = [
    path("", views.home),
    path("recipes/<int:id>/", views.recipe, name="recipe"),
    path(
        "recipes/category/<int:category_id>/",
        views.category,
        name="category",
    ),
]
