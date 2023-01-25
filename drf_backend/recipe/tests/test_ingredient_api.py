"""
Tests for the ingredients API.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Recipe

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    """Create and return an ingredient detail URL."""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def create_user(email='user@example.com', password='password'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicIngredientsAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that login is required for retrieving ingredients."""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients."""
        Ingredient.objects.create(user=self.user, name='salt')
        Ingredient.objects.create(user=self.user, name='sugar')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """Test that list of ingredients is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Ingredient.objects.create(user=user2, name='pepper')
        ingredient = Ingredient.objects.create(user=self.user, name='cumin')

        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        """Test updating an ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='tomato')

        payload = {'name': 'potato'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """Test deleting an ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='bread')
        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredient.objects.filter(user=self.user).exists())

    def test_filter_ingredients_assigned_to_recipe(self):
        """Test listing ingredients by those assigned to recipes."""
        ingredient_1 = Ingredient.objects.create(user=self.user, name='orange')
        ingredient_2 = Ingredient.objects.create(user=self.user, name='salt')
        recipe = Recipe.objects.create(
            title='orange juice',
            time_minutes=10,
            price=Decimal('6.40'),
            user=self.user
        )
        recipe.ingredients.add(ingredient_1)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        serializer_1 = IngredientSerializer(ingredient_1)
        serializer_2 = IngredientSerializer(ingredient_2)

        self.assertIn(serializer_1.data, res.data)
        self.assertNotIn(serializer_2.data, res.data)

    def test_filtered_ingredients_unique(self):
        """Test that filtering ingredients returns unique items."""
        ingredient = Ingredient.objects.create(user=self.user, name='tomato')
        Ingredient.objects.create(user=self.user, name='apple')
        recipe_1 = Recipe.objects.create(
            title='apple juice',
            time_minutes=6,
            price=Decimal('4.00'),
            user=self.user
        )
        recipe_2 = Recipe.objects.create(
            title='apple pie',
            time_minutes=70,
            price=Decimal('9.00'),
            user=self.user
        )
        recipe_1.ingredients.add(ingredient)
        recipe_2.ingredients.add(ingredient)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
