"""
Django admin customization for Trees app.
"""
from django.contrib import admin

from tree import models


class PlantedTreeInline(admin.TabularInline):
    """Inline table for PlantedTrees for a Tree."""
    model = models.PlantedTree
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


class LocationInLine(admin.TabularInline):
    """Inline table for Location of a PlantedTree."""
    model = models.Location
    extra = 0


class TreeAdmin(admin.ModelAdmin):
    """Define the admin page for trees."""
    inlines = [PlantedTreeInline]


class PlantedTreeAdmin(admin.ModelAdmin):
    """Define the admin page for planted trees."""
    inlines = [LocationInLine]


admin.site.register(models.Tree, TreeAdmin)
admin.site.register(models.PlantedTree, PlantedTreeAdmin)
