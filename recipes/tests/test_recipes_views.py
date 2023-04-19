from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views
from recipes.models import Category, Recipe


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_is_correct(self):
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_details_view_is_correct(self):
        view = resolve(reverse("recipes:recipe", kwargs={"id": 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_home_view_returns_code_200_ok(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_shows_no_recipes_found_if_no_recipe(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertIn("No recipes found!", response.content.decode("utf-8"))

    def test_recipe_home_view_loads_template_correct(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_category_view_returns_code_404_ok(self):
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_returns_code_404_ok(self):
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"id": 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_home_template_loads_recipe(self):
        category = Category.objects.create(name="Test Category")
        author = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
            email="email@email.com",
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title="Test Recipe",
            description="Test Description",
            slug="test-recipe",
            preparation_time=10,
            preparation_time_unit="minutos",
            servings=2,
            servings_unit="pessoas",
            preparation_steps="Test Preparation Steps",
            preparation_steps_is_html=False,
            is_published=True,
        )

        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipes"]

        self.assertIn("Test Recipe", content)
        self.assertIn("10 minutos", content)
        self.assertEqual(len(response_context_recipes), 1)
