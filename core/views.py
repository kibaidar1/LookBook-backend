from django.shortcuts import render
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import status, filters

from core.models import Look, Clothes
from core.serializers import LookSerializer, ClothesSerializer


class ReadOnlyLooksViewSet(ReadOnlyModelViewSet):
    search_fields = ['name', 'gender', 'author__username', 'created_at']
    filter_backends = (filters.SearchFilter,)
    # permission_classes = [DjangoModelPermissions]
    queryset = Look.objects.all()
    serializer_class = LookSerializer
    lookup_field = 'slug'


class ReadOnlyClothesViewSet(ReadOnlyModelViewSet):
    search_fields = ['name', 'colour', 'gender', 'author__username', 'created_at']
    filter_backends = (filters.SearchFilter,)
    # permission_classes = [DjangoModelPermissions]
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer
    lookup_field = 'slug'
