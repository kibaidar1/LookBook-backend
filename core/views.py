from django.shortcuts import render
from nested_multipart_parser.drf import DrfNestedParser
from rest_framework.generics import CreateAPIView, get_object_or_404, \
    RetrieveDestroyAPIView
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import status, filters

from core.models import Look, Clothes, LookImages
from core.permissions import IsAuthorOrReadOnly, LookIsAuthorOrReadOnly
from core.serializers import LookSerializer, ClothesSerializer, LookImagesSerializer


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


class MyLooksViewSet(ModelViewSet):
    serializer_class = LookSerializer
    permission_classes = [DjangoModelPermissions, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Look.objects.filter(author=self.request.user)


class ImageCreateAPIView(CreateAPIView):
    serializer_class = LookImagesSerializer
    permission_classes = [DjangoModelPermissions, IsAuthorOrReadOnly]
    queryset = LookImages.objects.all()

    def perform_create(self, serializer):
        look_slug = self.kwargs['look_slug']
        look = get_object_or_404(queryset=Look, author=self.request.user, slug=look_slug)
        return serializer.save(look=look)


class ImageRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = LookImagesSerializer
    permission_classes = [DjangoModelPermissions, LookIsAuthorOrReadOnly]
    # lookup_field = 'pk'

    def get_queryset(self):
        look_slug = self.kwargs['look_slug']
        look = get_object_or_404(queryset=Look, author=self.request.user, slug=look_slug)
        return LookImages.objects.filter(look=look)


class MyClothesViewSet(ModelViewSet):
    serializer_class = ClothesSerializer
    permission_classes = [DjangoModelPermissions, IsAuthorOrReadOnly]
    lookup_field = 'slug'
    parser_classes = (DrfNestedParser, MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        print(self.request.data)
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Clothes.objects.filter(author=self.request.user)
