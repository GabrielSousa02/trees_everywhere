"""
Django admin customization for Trees app.
"""
from django.contrib import admin

from tree import models


class PlantedTreeInline(admin.TabularInline):
    """Inline table for PlantedTrees for a Tree"""
    model = models.PlantedTree
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


class TreeAdmin(admin.ModelAdmin):
    """Define the admin page for trees."""
    inlines = [PlantedTreeInline]


admin.site.register(models.Tree, TreeAdmin)
admin.site.register(models.PlantedTree)
