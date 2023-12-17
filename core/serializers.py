from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import User, Look, Clothes, ClothesLink, LookImages, Comment, ClothesCategory


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = "__all__"


class ClothesLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesLink
        fields = ['id', 'link']


class ClothesSerializer(WritableNestedModelSerializer):
    author = serializers.HiddenField(default=CurrentUserDefault())
    authors_name = serializers.ReadOnlyField(source='author.username')
    links = ClothesLinkSerializer(many=True, required=False)
    read_only_fields = ['images', 'created_at', 'author']

    class Meta:
        model = Clothes
        fields = ['id', 'name', 'slug', 'colour', 'gender', 'links', 'author', 'authors_name', 'created_at']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ClothesCategorySerializer(WritableNestedModelSerializer):
    clothes = ClothesSerializer(many=True, required=False)

    class Meta:
        model = ClothesCategory
        fields = ['id', 'name', 'clothes']


class LookImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookImages
        fields = ['id', 'image']


class LookSerializer(WritableNestedModelSerializer):
    images = LookImagesSerializer(many=True, read_only=True)
    clothes_category = ClothesCategorySerializer(many=True, required=False)
    author = serializers.HiddenField(default=CurrentUserDefault())
    authors_name = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    read_only_fields = ['images', 'created_at', 'author']
    likes = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Look
        fields = ['id', 'name', 'slug', 'gender', 'description',  'images', 'clothes_category', 'created_at',
                  'author', 'authors_name', 'likes', 'comments']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class RegistrationUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"detail": "Пароли не совпадают"})
        user.set_password(password)
        user.save()
        return user


