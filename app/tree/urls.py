"""
URLs mapping for Tree API.
"""
from django.urls import path

from tree import views


urlpatterns = [
    path('', views.PlantedTreeListAPIView.as_view(), name='planted-tree-list'),
]
