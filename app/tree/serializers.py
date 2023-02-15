"""
Serializers for Tree APIs
"""
from rest_framework import serializers

from tree.models import PlantedTree


class PlantedTreeSerializer(serializers.ModelSerializer):
    """Serializer for PlantedTrees."""

    class Meta:
        model = PlantedTree
        fields = '__all__'
        read_only_fields = ['id']
