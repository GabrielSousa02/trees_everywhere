"""
Tests for Tree APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from tree.models import Tree, PlantedTree

from tree.serializers import PlantedTreeSerializer


TREES_URL = reverse('planted_trees:planted-tree-list')


class TreeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        result = self.client.get(TREES_URL)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTreeAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
            'User',
        )
        self.tree = Tree.objects.create(
            name="Oak Tree",
            scientific_name="Quercus",
        )
        self.client.force_authenticate(self.user)
        tree_for_planting = [('Oak Tree', (40.744801, -111.875066))]
        self.user.plant_tree(tree=tree_for_planting)

    def test_retrieve_trees(self):
        self.user.plant_tree(tree=[('Oak Tree', (33.589472, -117.813085))])
        result = self.client.get(TREES_URL)

        planted_trees = PlantedTree.objects.all().order_by('-id')
        serializer = PlantedTreeSerializer(planted_trees, many=True)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_tree_list_limited_to_user(self):
        """Test list of trees is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'passcode123',
            'Other user',
        )
        other_user.plant_tree(tree=[('Oak Tree', (37.577240, 126.977022))])

        result = self.client.get(TREES_URL)

        planted_trees = PlantedTree.objects.filter(user=self.user)
        serializer = PlantedTreeSerializer(planted_trees, many=True)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)
