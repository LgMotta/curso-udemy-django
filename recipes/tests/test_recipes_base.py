from django.contrib.auth.models import User
from django.test import TestCase

from recipes.models import Category, Recipe


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_category(self, name="Test Category"):
        return Category.objects.create(name=name)

    def make_author(
        self,
        username="testuser",
        password="testpassword",
        first_name="Test",
        last_name="User",
        email="email@email.com",
    ):
        return User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
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
        cover_image="None",
    ):

        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            cover=cover_image,
        )
