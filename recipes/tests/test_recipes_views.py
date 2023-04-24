from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipes_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_view_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_code_200_ok(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_shows_no_recipes_found_if_no_recipe(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertIn("No recipes found!", response.content.decode("utf-8"))

    def test_recipe_home_view_loads_template_correct(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_home_dont_loads_not_published_recipes(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse("recipes:home"))

        self.assertIn("No recipes found!", response.content.decode("utf-8"))

    def test_recipe_category_view_returns_code_404_ok(self):
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_is_correct(self):
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_loads_template_correct(self):
        needed_title = "This is category test"
        self.make_recipe(title=needed_title)
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1})
        )
        content = response.content.decode("utf-8")

        self.assertIn(needed_title, content)

    def test_recipe_category_dont_loads_not_published_recipes(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(
                "recipes:category", kwargs={"category_id": recipe.category.id}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_is_correct(self):
        view = resolve(reverse("recipes:recipe", kwargs={"id": 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_code_404_ok(self):
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"id": 1000})
        )
        self.assertEqual(response.status_code, 404)
        self.make_recipe(preparation_time=7)
        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipes"]

        self.assertIn("Test Recipe", content)
        self.assertIn("7 minutos", content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_detail_view_loads_correct_recipe(self):
        needed_title = "this is a detail page - it loads the correct recipe"
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse("recipes:recipe", kwargs={"id": 1}))
        content = response.content.decode("utf-8")

        self.assertIn(needed_title, content)

    def test_recipe_detail_dont_loads_not_published_recipes(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"id": recipe.id})
        )

        self.assertEqual(response.status_code, 404)
