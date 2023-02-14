"""
Test for Tree models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from tree.models import Tree


class ModelTests(TestCase):
    """Test Tree models."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User',
            user_about='User'
        )
        self.tree = Tree.objects.create(
            name="Oak Tree",
            scientific_name="Quercus",
        )

    def test_tree_create_sucess(self):
        """Test the successful creation of a tree."""
        name = "European Oak Tree"
        scientific_name = "Quercus robur"
        created_tree = Tree.objects.create(
            name=name,
            scientific_name=scientific_name,
        )

        self.assertEqual(created_tree.name, name)
        self.assertEqual(created_tree.scientific_name, scientific_name)

    def test_successful_planted_tree(self):
        """Test successful PlantedTree."""
        tree_for_planting = [('Oak Tree', (-27.609895, -48.531859))]
        result = self.user.plant_tree(tree=tree_for_planting)

        self.assertTrue(result[0])
        self.assertEqual(result[1].name, 'Oak Tree')
        self.assertEqual(result[1].location, (-27.609895, -48.531859))
