"""
Tests for the tags API.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Recipe

from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


def create_user(email='user@example.com', password='password123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


def detail_url(tag_id):
    """Create and return tag details url."""
    return reverse('recipe:tag-detail', args=[tag_id])


class PublicTagsAPITests(TestCase):
    """TEst unauthenticated tag API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required for retrieving tags."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """TEst authenticated tag API requests"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving a list of tags"""
        Tag.objects.create(user=self.user, name='Tag1')
        Tag.objects.create(user=self.user, name='Tag2')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Tag.objects.create(user=user2, name='TagUser2')
        tag = Tag.objects.create(user=self.user, name='TagUser')
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        """Test updating a tag."""
        tag = Tag.objects.create(user=self.user, name='Old Tag')

        payload = {'name': 'New Tag'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(res.data['name'], payload['name'])

    def test_delete_tag(self):
        """Test deleting a tag."""
        tag = Tag.objects.create(user=self.user, name='Tag')
        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(user=self.user).exists())

    def test_filter_tags_assigned_to_recipes(self):
        """Test listing tags by those assigned to recipes."""
        tag_1 = Tag.objects.create(user=self.user, name='brunch')
        tag_2 = Tag.objects.create(user=self.user, name='dinner')
        recipe = Recipe.objects.create(
            title='omelette',
            time_minutes=15,
            price=Decimal('4.50'),
            user=self.user
        )
        recipe.tags.add(tag_1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        serializer_1 = TagSerializer(tag_1)
        serializer_2 = TagSerializer(tag_2)

        self.assertIn(serializer_1.data, res.data)
        self.assertNotIn(serializer_2.data, res.data)

    def test_filtered_tags_unique(self):
        """Test filtered tags returns unique items."""
        tag = Tag.objects.create(user=self.user, name='breakfast')
        Tag.objects.create(user=self.user, name='lunch')
        recipe_1 = Recipe.objects.create(
            title='scrambled eggs',
            time_minutes=8,
            price=Decimal('2.30'),
            user=self.user
        )
        recipe_2 = Recipe.objects.create(
            title='sandwich',
            time_minutes=30,
            price=Decimal('6.50'),
            user=self.user
        )
        recipe_1.tags.add(tag)
        recipe_2.tags.add(tag)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)