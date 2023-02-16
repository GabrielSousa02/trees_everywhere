"""
URLs mapping for Tree API.
"""
from django.urls import path

from tree import views


urlpatterns = [
    # Tree APIs
    path(
        'api/planted_trees',
        views.PlantedTreeListAPIView.as_view(),
        name='planted-tree-list'
    ),

    # Tree View Templates
    path(
        '',
        views.TreeHomeTemplateView.as_view(),
        name='trees-home'
    ),
    path(
        'plant_new_tree',
        views.create_planted_tree,
        name='create-planted-tree',
    ),
    path(
        'planted_trees/',
        views.PlantedTreeListView.as_view(),
        name='list-planted'
    ),
    path(
        'planted_tree_detail/<int:pk>',
        views.PlantedTreeDetailView.as_view(),
        name='detail-planted',
    ),
    path(
        'planted_tree_update/<int:pk>',
        views.PlantedTreeUpdateView.as_view(),
        name='update_planted',
    ),
]
