from django.core.exceptions import ValidationError
from parameterized import parameterized

from recipes.models import Recipe
from recipes.tests.test_recipes_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        return Recipe(
            category=self.make_category(name="teste categoria 1"),
            author=self.make_author(username="teste usuario 1"),
            title="Test Recipe",
            description="Test Description",
            slug="test-recipe",
            preparation_time=10,
            preparation_time_unit="minutos",
            servings=2,
            servings_unit="pessoas",
            preparation_steps="Test Preparation Steps",
            cover="None",
        )

    @parameterized.expand(
        [
            ("title", 65),
            ("description", 165),
            ("preparation_time_unit", 65),
            ("servings_unit", 65),
        ]
    )
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, "a" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_is_published_is_default_false(self):
        recipe = self.make_recipe_no_defaults()

        recipe.full_clean()
        recipe.save()
        self.assertFalse(
            recipe.is_published, msg="is_published should be False by default"
        )

    def test_preparation_steps_is_html_is_default_false(self):
        recipe = self.make_recipe_no_defaults()

        recipe.full_clean()
        recipe.save()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg="preparation_steps_is_html should be False by default",
        )

    def test_recipe_str_representation(self):
        test_title = "Test Recipe"
        self.recipe.title = test_title
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), test_title)
