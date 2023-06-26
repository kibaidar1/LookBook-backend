from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import User, Look, Clothes, ClothesLink


class ClothesLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesLink
        fields = ['link']


class ClothesSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    links = serializers.ReadOnlyField(source='links.link')

    class Meta:
        model = Clothes
        fields = ['name', 'description', 'gender', 'image', 'links', 'slug', 'updated_at', 'author']
        read_only_fields = ['author']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class LookSerializer(serializers.ModelSerializer):
    clothes = ClothesSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Look
        fields = ['name', 'description', 'gender', 'image', 'clothes', 'slug', 'updated_at', 'author']
        read_only_fields = ['author',]
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
