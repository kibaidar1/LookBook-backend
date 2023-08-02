from rest_framework.generics import CreateAPIView, get_object_or_404, \
    RetrieveDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import status, filters

from core.models import Look, Clothes, LookImages, ClothesLink, Comment, User
from core.permissions import IsAuthorOrReadOnly, LookIsAuthorOrReadOnly, ClothesIsAuthorOrReadOnly
from core.serializers import LookSerializer, ClothesSerializer, LookImagesSerializer, ClothesLinkSerializer, \
    CommentSerializer, RegistrationUserSerializer


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
        return serializer.save(author=self.request.user)

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


class LookImagesRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = LookImagesSerializer
    permission_classes = [DjangoModelPermissions, LookIsAuthorOrReadOnly]
    # lookup_field = 'pk'

    def get_queryset(self):
        look_slug = self.kwargs['look_slug']
        look = get_object_or_404(queryset=Look, author=self.request.user, slug=look_slug)
        return LookImages.objects.filter(look=look)


class MyClothesViewSet(ModelViewSet):
    serializer_class = ClothesSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        return Clothes.objects.filter(author=self.request.user)


class ClothesLinkRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = ClothesLinkSerializer
    permission_classes = [DjangoModelPermissions, ClothesIsAuthorOrReadOnly]

    # lookup_field = 'pk'

    def get_queryset(self):
        clothes_slug = self.kwargs['clothes_slug']
        clothes = get_object_or_404(queryset=Clothes, author=self.request.user, slug=clothes_slug)
        return ClothesLink.objects.filter(clothes=clothes)


class MyCommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [DjangoModelPermissions, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


class RegistrationUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationUserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = f'{request.data["username"]}, you are registered'
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


