from drf_writable_nested import WritableNestedModelSerializer
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


class ClothesSerializer(WritableNestedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    links = ClothesLinkSerializer(many=True, required=False)
    read_only_fields = ['images', 'created_at', 'author']

    class Meta:
        model = Clothes
        fields = ['id', 'name', 'slug', 'colour', 'gender', 'description', 'links', 'author', 'created_at']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class LookImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookImages
        fields = ['id', 'image']


class LookSerializer(WritableNestedModelSerializer):
    clothes = ClothesSerializer(many=True, required=False)
    images = LookImagesSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    read_only_fields = ['images', 'created_at', 'author']
    likes = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Look
        fields = ['id', 'name', 'slug', 'gender', 'description',  'images', 'clothes', 'created_at', 'author',
                  'likes', 'comments']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class RegistrationUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        # fields = ['email', 'username', 'password', 'password2']
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


