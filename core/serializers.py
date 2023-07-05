from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import User, Look, Clothes, ClothesLink


class ClothesLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesLink
        fields = ['link']


class ClothesSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    links = ClothesLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Clothes
        fields = ['name', 'slug', 'gender', 'description', 'image', 'links', 'author', 'created_at']
        read_only_fields = ['author']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class LookSerializer(serializers.ModelSerializer):
    clothes = ClothesSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Look
        fields = ['name', 'description', 'gender', 'image', 'clothes', 'slug', 'created_at', 'author']
        read_only_fields = ['author']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
