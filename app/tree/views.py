"""
Views for the Tree and PlantedTree.
"""
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import formset_factory
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    UpdateView,
)
from rest_framework.generics import ListAPIView
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication
)
from rest_framework.permissions import IsAuthenticated

from tree.models import PlantedTree
from tree import forms
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


class TreeHomeTemplateView(TemplateView):
    template_name = 'trees/tree_home.html'


class PlantedTreeListView(ListView):
    model = PlantedTree
    context_object_name = 'trees_list'


class PlantedTreeDetailView(DetailView):
    model = PlantedTree


class PlantedTreeUpdateView(UpdateView):
    model = PlantedTree


def create_planted_tree(request):
    form = forms.PlantedTreeForm(request.POST or None)
    LocationFormSet = formset_factory(forms.LocationForm)
    formset = LocationFormSet(request.POST or None)

    context = {
        'form': form,
        'formset': formset,
    }
    if request.method == 'POST':
        if form.is_valid():
            planted_tree = form.save(commit=False)
            planted_tree.user = request.user
            planted_tree.save()

            for form in formset:
                location = form.save(commit=False)
                location.planted_tree = planted_tree

                location.save()
            return redirect(reverse('trees:list-planted'))
    return render(request, "tree/plantedtree_form.html", context=context)
