"""
Test for Tree models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from tree.models import Tree
from account.models import Account


class ModelTests(TestCase):
    """Test Tree models."""

    def setUp(self):
        self.account = Account.objects.create(
            name='Sample Account 01'
        )
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

        self.account.add_member(self.user)

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
        tree_for_planting = [('Oak Tree', (40.744801, -111.875066))]
        result = self.user.plant_tree(tree=tree_for_planting)

        self.assertTrue(result[0])
        self.assertEqual(result[1].tree.name, 'Oak Tree')
        self.assertEqual(result[1].location.latitude, 40.744801)
        self.assertEqual(result[1].location.longitude, -111.875066)

        # Check that the user ha the tree linked in DB
        user_trees = [tree for tree in self.user.user_trees.all()]

        self.assertTrue(user_trees)
        self.assertEqual(len(user_trees), 1)

    def test_successful_multiple_planted_trees(self):
        """Test successful multiple PlantedTree."""
        trees_for_planting = [
            ('Oak Tree', (40.744801, -111.875066)),
            ('Oak Tree', (33.589472, -117.813085)),
            ('Oak Tree', (37.577240, 126.977022)),
        ]
        result = self.user.plant_trees(trees=trees_for_planting)

        # Checking first tree planted
        self.assertTrue(result[0][0])
        self.assertEqual(result[0][1].tree.name, 'Oak Tree')
        self.assertEqual(result[0][1].location.latitude, 40.744801)
        self.assertEqual(result[0][1].location.longitude, -111.875066)

        # Checking second tree planted
        self.assertTrue(result[1][0])
        self.assertEqual(result[1][1].tree.name, 'Oak Tree')
        self.assertEqual(result[1][1].location.latitude, 33.589472)
        self.assertEqual(result[1][1].location.longitude, -117.813085)

        # Checking third tree planted
        self.assertTrue(result[2][0])
        self.assertEqual(result[2][1].tree.name, 'Oak Tree')
        self.assertEqual(result[2][1].location.latitude, 37.577240)
        self.assertEqual(result[2][1].location.longitude, 126.977022)

        # Check that the user has the trees linked in DB
        user_trees = [tree for tree in self.user.user_trees.all()]

        self.assertTrue(user_trees)
        self.assertEqual(len(user_trees), 3)

    def test_partial_success_multiple_planted_trees(self):
        """Test partial success multiple PlantedTree."""
        trees_for_planting = [
            ('Oak Tree', (40.744801, -111.875066)),
            ('No Tree', (33.589472, -117.813085)),
            ('Oak Tree', (37.577240, 126.977022)),
        ]
        result = self.user.plant_trees(trees=trees_for_planting)

        # Checking first tree planted
        self.assertTrue(result[0][0])
        self.assertEqual(result[0][1].tree.name, 'Oak Tree')
        self.assertEqual(result[0][1].location.latitude, 40.744801)
        self.assertEqual(result[0][1].location.longitude, -111.875066)

        # Checking second tree planted
        self.assertFalse(result[1][0])
        self.assertEqual(result[1][1], ObjectDoesNotExist)

        # Checking third tree planted
        self.assertTrue(result[2][0])
        self.assertEqual(result[2][1].tree.name, 'Oak Tree')
        self.assertEqual(result[2][1].location.latitude, 37.577240)
        self.assertEqual(result[2][1].location.longitude, 126.977022)
