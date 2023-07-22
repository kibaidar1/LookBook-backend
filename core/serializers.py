from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import User, Look, Clothes, ClothesLink, LookImages, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = "__all__"


class ClothesLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesLink
        fields = ['id', 'link']


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

    def create(self, validated_data):
        links = validated_data.pop('links')
        clothes = Clothes.objects.create(**validated_data)
        for link in links:
            ClothesLink.objects.create(clothes=clothes, **link)
        return clothes


class LookImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookImages
        fields = ['id', 'image']


class LookSerializer(serializers.ModelSerializer):
    clothes = ClothesSerializer(many=True, read_only=True)
    images = LookImagesSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    read_only_fields = ['images', 'created_at', 'author']

    class Meta:
        model = Look
        # fields = ['name', 'description', 'gender', 'images', 'clothes', 'slug', 'created_at', 'author']
        fields = '__all__'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


