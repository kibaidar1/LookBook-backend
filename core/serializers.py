from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import User, Look, Clothes, ClothesLink, LookImages


class ClothesLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesLink
        fields = ['link']


class ClothesSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    links = ClothesLinkSerializer(many=True, required=False)
    read_only_fields = ['images', 'created_at', 'author']

    class Meta:
        model = Clothes
        # fields = ['name', 'slug', 'colour', 'gender', 'description', 'links', 'author', 'created_at']
        fields = '__all__'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class LookImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookImages
        fields = ['id', 'image']


class LookSerializer(serializers.ModelSerializer):
    clothes = ClothesSerializer(many=True, read_only=True)
    images = LookImagesSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    read_only_fields = ['images', 'created_at', 'author']

    class Meta:
        model = Look
        # fields = ['name', 'description', 'gender', 'images', 'clothes', 'slug', 'created_at', 'author']
        fields = '__all__'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


