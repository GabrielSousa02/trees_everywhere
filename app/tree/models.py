from django.db import models


class PlantedTree(models.Model):
    age = models.IntegerField()
    planted_at = models.DateTimeField()
    user = models.ForeignKey('core.user', on_delete=models.CASCADE)
    account = models.ForeignKey('account.account', on_delete=models.CASCADE)
    tree = models.ForeignKey('tree', on_delete=models.RESTRICT)

    def save(self, *args, **kwargs):
        latitude = kwargs.pop('latitude')
        longitude = kwargs.pop('longitude')
        super().save(*args, **kwargs)
        new_location = Location.objects.create(
            latitude=latitude,
            longitude=longitude,
        )
        new_location.save(planted_tree=self)


class Location(models.Model):
    planted_tree = models.OneToOneField(
        'plantedtree',
        primary_key=True,
        on_delete=models.CASCADE,
    )
    latitude = models.DecimalField(decimal_places=6, max_digits=12)
    longitude = models.DecimalField(decimal_places=6, max_digits=12)


class Tree(models.Model):
    name = models.CharField(max_length=255, unique=True)
    scientific_name = models.CharField(max_length=255, unique=True)
