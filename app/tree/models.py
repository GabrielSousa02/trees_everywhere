from django.db import models


class PlantedTree(models.Model):
    """Planted Tree for a Tree type."""
    age = models.IntegerField()
    planted_at = models.DateTimeField()
    user = models.ForeignKey(
        'core.user',
        on_delete=models.CASCADE,
        related_name='user_trees'
    )
    account = models.ManyToManyField(
        'account.account',
        blank=True,
        related_name='account_trees',
    )
    tree = models.ForeignKey(
        'tree',
        on_delete=models.RESTRICT,
        related_name='planted_trees',
    )

    def __str__(self):
        return f'Tree planted by {self.user}'


class Location(models.Model):
    """Location in Coordinates of a PlantedTree."""
    planted_tree = models.OneToOneField(
        'plantedtree',
        primary_key=True,
        on_delete=models.CASCADE,
    )
    latitude = models.DecimalField(decimal_places=6, max_digits=12)
    longitude = models.DecimalField(decimal_places=6, max_digits=12)


class Tree(models.Model):
    """Tree type."""
    name = models.CharField(max_length=255, unique=True)
    scientific_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
