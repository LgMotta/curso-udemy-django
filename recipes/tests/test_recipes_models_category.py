from django.core.exceptions import ValidationError

from recipes.tests.test_recipes_base import RecipeTestBase


class CategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(name="teste categoria")
        return super().setUp()

    def test_category_model_str_representation_is_name_field(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )

    def test_category_model_name_max_length(self):
        self.category.name = "a" * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
