"""
Django form for PlantedTree creation view.
"""
from django import forms

from tree.models import PlantedTree, Location


class DateInput(forms.DateInput):
    input_type = 'date'


class PlantedTreeForm(forms.ModelForm):
    class Meta:
        model = PlantedTree
        fields = ['age', 'planted_at', 'tree']

        widgets = {
            "planted_at": DateInput(),
        }

        labels = {
            'age': 'Tree Age',
            'planted_at': 'Planted At',
            'tree': 'Tree Name',
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude']

        labels = {
            'latitude': '*Latitude',
            'longitude': '*Longitude',
        }
