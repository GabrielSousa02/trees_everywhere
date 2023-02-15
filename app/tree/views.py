"""
Views for the Tree APIS.
"""
from rest_framework.generics import ListAPIView
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication
)
from rest_framework.permissions import IsAuthenticated

from tree.models import PlantedTree
from tree import serializers


class PlantedTreeListAPIView(ListAPIView):
    """View for list Tree API."""
    serializer_class = serializers.PlantedTreeSerializer
    queryset = PlantedTree.objects.all()
    authentication_classes = [
        BasicAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve planted trees for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
