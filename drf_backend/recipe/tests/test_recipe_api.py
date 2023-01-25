"""
Test for the recipe API.
"""
from decimal import Decimal
import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Create and return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def create_recipe(user, **params):
    """Create and return a recipe."""
    default_params = {
        'title': 'Test recipe title',
        'time_minutes': 10,
        'price': Decimal('10.00'),
        'description': 'Test recipe description',
        'link': 'http://example.com/recipe.pdf',
    }
    default_params.update(params)

    recipe = Recipe.objects.create(user=user, **default_params)
    return recipe


def image_upload_url(recipe_id):
    """Create and return image upload URL."""
    return reverse('recipe:recipe-upload-image', args=[recipe_id])


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated recipe API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to call API."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated recipe API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='password123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated users."""
        other_user = create_user(
            email='other@example.com',
            password='password123'
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe through the API."""
        payload = {
            'title': 'Sample recipe',
            'time_minutes': 20,
            'price': Decimal('15.50'),
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update_recipe(self):
        """Test partial update of a recipe with patch."""
        original_link = 'http://example.com/recipe.pdf'
        recipe = create_recipe(
            user=self.user,
            title='Sample recipe 2',
            link=original_link
        )

        payload = {'title': 'New recipe title'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update_recipe(self):
        """Test full update of a recipe with put."""
        recipe = create_recipe(
            user=self.user,
            title='Sample recipe 4',
            link='http://example.com/recipe.pdf',
            description='Sample recipe description'
        )

        payload = {
            'title': 'New recipe title',
            'link': 'http://example.com/new-recipe.pdf',
            'description': 'New description',
            'time_minutes': 22,
            'price': Decimal('13.00')
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the recipe user results in an error - user cannot be changed."""
        new_user = create_user(
            email='new@example.com',
            password='password123'
        )
        recipe = create_recipe(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Test deleting a recipe."""
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_other_users_recipe_error(self):
        """Test trying to delete a recipe of another user gives error."""
        new_user = create_user(
            email='new@example.com',
            password='password123'
        )
        recipe = create_recipe(user=new_user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())

    def test_create_recipe_with_new_tags(self):
        """Test creating a recipe with new tags."""
        payload = {
            'title': 'Chicken',
            'time_minutes': 20,
            'price': Decimal('8.50'),
            'tags': [
                {'name': 'chicken'},
                {'name': 'spicy'},
            ]
        }
        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes.first()
        self.assertEqual(recipe.tags.count(), 2)
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name=tag['name'],
                user=self.user
            ).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_existing_tags(self):
        """Test creating a recipe with existing tag."""
        tag_chicken = Tag.objects.create(user=self.user, name='chicken')
        payload = {
            'title': 'Chicken',
            'time_minutes': 30,
            'price': Decimal('11.50'),
            'tags': [
                {'name': 'chicken'},
                {'name': 'dinner'}
            ]
        }
        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes.first()
        self.assertEqual(recipe.tags.count(), 2)
        self.assertIn(tag_chicken, recipe.tags.all())
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name=tag['name'],
                user=self.user
            ).exists()
            self.assertTrue(exists)

    def test_tag_on_update(self):
        """Test creating a tag when updating a recipe."""
        recipe = create_recipe(user=self.user)

        payload = {'tags': [{'name': 'lunch'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_tag = Tag.objects.get(user=self.user, name='lunch')
        self.assertIn(new_tag, recipe.tags.all())

    def test_update_recipe_assign_tag(self):
        """Test assigning an existing tag when updating a recipe."""
        tag_fish = Tag.objects.create(user=self.user, name='fish')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag_fish)

        tag_beef = Tag.objects.create(user=self.user, name='beef')
        # change all tags to list below (not add)
        payload = {'tags': [{'name': 'beef'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_beef, recipe.tags.all())
        self.assertNotIn(tag_fish, recipe.tags.all())

    def test_clear_recipe_tags(self):
        """Test clearing recipes tags."""
        tag = Tag.objects.create(user=self.user, name='milk')
        recipe = create_recipe(user=self.user)
        payload = {'tags': []}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 0)

    def test_create_recipe_with_new_ingredients(self):
        """Test creating a recipe with new ingredients."""
        payload = {
            'title': 'Salad',
            'time_minutes': 20,
            'price': Decimal('12.50'),
            'ingredients': [
                {'name': 'chicken'},
                {'name': 'tomato'},
            ]
        }
        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes.first()
        self.assertEqual(recipe.ingredients.count(), 2)
        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(
                name=ingredient['name'],
                user=self.user
            ).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_existing_ingredients(self):
        """Test creating a recipe with existing ingredients."""
        ingredient = Ingredient.objects.create(
            name='coffee',
            user=self.user,
        )

        payload = {
            'title': 'Coffee',
            'time_minutes': 20,
            'price': Decimal('3.50'),
            'ingredients': [
                {'name': 'coffee'},
                {'name': 'milk'},
            ]
        }
        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes.first()
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertIn(ingredient, recipe.ingredients.all())
        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(
                name=ingredient['name'],
                user=self.user
            ).exists()
            self.assertTrue(exists)

    def test_create_ingredient_on_update(self):
        """Test creating an ingredient when updating a recipe."""
        recipe = create_recipe(user=self.user)

        payload = {'ingredients': [{'name': 'lemons'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient = Ingredient.objects.get(user=self.user, name='lemons')
        self.assertIn(ingredient, recipe.ingredients.all())
        self.assertEqual(recipe.ingredients.count(), 1)
        self.assertEqual(ingredient.name, payload['ingredients'][0]['name'])

    def test_update_recipe_assign_ingredient(self):
        """Test assigning an existing ingredient when updating a recipe."""
        ingredient_1 = Ingredient.objects.create(
            user=self.user,
            name='almonds',
        )
        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient_1)
        ingredient_2 = Ingredient.objects.create(
            user=self.user,
            name='eggs'
        )
        payload = {'ingredients': [{'name': 'eggs'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.ingredients.count(), 1)
        self.assertIn(ingredient_2, recipe.ingredients.all())
        self.assertNotIn(ingredient_1, recipe.ingredients.all())

    def test_clear_ingredients(self):
        """Test clearing a recipes ingredients."""
        ingredient = Ingredient.objects.create(
            user=self.user,
            name='oregano',
        )
        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient)
        payload = {'ingredients': []}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.ingredients.count(), 0)

    def test_filter_by_tags(self):
        """Test filtering recipes by tags."""
        recipe_1 = create_recipe(user=self.user, title='burger')
        recipe_2 = create_recipe(user=self.user, title='cheeseburger')
        tag_1 = Tag.objects.create(user=self.user, name='beef')
        tag_2 = Tag.objects.create(user=self.user, name='cheese')
        recipe_1.tags.add(tag_1)
        recipe_2.tags.add(tag_2)
        recipe_3 = create_recipe(user=self.user, title='french fries')

        params = {'tags': f'{tag_1.id},{tag_2.id}'}
        res = self.client.get(RECIPES_URL, params)
        serializer_1 = RecipeSerializer(recipe_1)
        serializer_2 = RecipeSerializer(recipe_2)
        serializer_3 = RecipeSerializer(recipe_3)

        self.assertIn(serializer_1.data, res.data)
        self.assertIn(serializer_2.data, res.data)
        self.assertNotIn(serializer_3.data, res.data)

    def test_filter_by_ingredients(self):
        """Test filtering recipes by ingredients."""
        recipe_1 = create_recipe(user=self.user, title='scrambled eggs')
        recipe_2 = create_recipe(user=self.user, title='pizza pepperoni')
        ingredient_1 = Ingredient.objects.create(user=self.user, name='eggs')
        ingredient_2 = Ingredient.objects.create(user=self.user, name='cheese')
        recipe_1.ingredients.add(ingredient_1)
        recipe_2.ingredients.add(ingredient_2)
        recipe_3 = create_recipe(user=self.user, title='chicken curry')

        params = {'ingredients': f'{ingredient_1.id},{ingredient_2.id}'}
        res = self.client.get(RECIPES_URL, params)

        serializer_1 = RecipeSerializer(recipe_1)
        serializer_2 = RecipeSerializer(recipe_2)
        serializer_3 = RecipeSerializer(recipe_3)

        self.assertIn(serializer_1.data, res.data)
        self.assertIn(serializer_2.data, res.data)
        self.assertNotIn(serializer_3.data, res.data)


class ImageUploadTests(TestCase):
    """Test for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='password123',
        )
        self.client.force_authenticate(self.user)
        self.recipe = create_recipe(user=self.user)

    def tearDown(self):
        self.recipe.image.delete()

    def test_upload_image_to_recipe(self):
        """Test uploading an image to recipe."""
        url = image_upload_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')
        self.recipe.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image."""
        url = image_upload_url(self.recipe.id)
        payload = {'image': 'not an image'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
