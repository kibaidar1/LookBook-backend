from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import CreateAPIView, get_object_or_404, \
    RetrieveDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import status, filters

from core.models import Look, Clothes, LookImages, Comment, User
from core.permissions import IsAuthorOrReadOnly, LookIsAuthorOrReadOnly
from core.serializers import LookSerializer, ClothesSerializer, LookImagesSerializer, \
    CommentSerializer, RegistrationUserSerializer


@extend_schema(tags=['Looks'])
@extend_schema_view(
    list=extend_schema(
            summary="Получение списка образов",
        ),
)
class ReadOnlyLooksViewSet(ReadOnlyModelViewSet):
    search_fields = ['name', 'gender', 'author__username', 'created_at']
    filter_backends = (filters.SearchFilter,)
    queryset = Look.objects.all()
    serializer_class = LookSerializer
    lookup_field = 'slug'


@extend_schema(tags=['Clothes'])
@extend_schema_view(
    list=extend_schema(
            summary="Получение списка вещей",
        ),
)
class ReadOnlyClothesViewSet(ReadOnlyModelViewSet):
    search_fields = ['name', 'colour', 'gender', 'author__username', 'created_at']
    filter_backends = (filters.SearchFilter,)
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer
    lookup_field = 'slug'


@extend_schema(tags=['Looks'])
@extend_schema_view(
    list=extend_schema(
            summary="Получение списка моих образов",
    ),
    update=extend_schema(
        summary="Изменение моего образ",
    ),
    create=extend_schema(
            summary="Создание нового образа",
    ),
    delete=extend_schema(
        summary="Удаление моего образа"
    )
)
class MyLooksViewSet(ModelViewSet):
    serializer_class = LookSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        return Look.objects.filter(author=self.request.user)


@extend_schema(tags=['Looks'])
@extend_schema_view(
    create=extend_schema(
        summary="Добавление изобржений к образу",
    ),
)
class ImageCreateAPIView(CreateAPIView):
    serializer_class = LookImagesSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = LookImages.objects.all()

    def perform_create(self, serializer):
        look_slug = self.kwargs['look_slug']
        look = get_object_or_404(queryset=Look, author=self.request.user, slug=look_slug)
        return serializer.save(look=look)


@extend_schema(tags=['Looks'])
@extend_schema_view(
    get=extend_schema(
        summary="Получение изобржений образа"
    ),
    delete=extend_schema(
        summary="Удаление изображения из образа"
    )
)
class LookImagesRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = LookImagesSerializer
    permission_classes = [IsAuthenticated, LookIsAuthorOrReadOnly]

    def get_queryset(self):
        look_slug = self.kwargs['look_slug']
        look = get_object_or_404(queryset=Look, author=self.request.user, slug=look_slug)
        return LookImages.objects.filter(look=look)


@extend_schema(tags=['Clothes'])
@extend_schema_view(
    list=extend_schema(
            summary="Получение списка моих вещей",
    ),
    update=extend_schema(
        summary="Изменение моей вещи",
    ),
    create=extend_schema(
            summary="Добавление новой вещи",
    ),
    delete=extend_schema(
        summary="Удаление моей вещи"
    )
)
class MyClothesViewSet(ModelViewSet):
    serializer_class = ClothesSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        return Clothes.objects.filter(author=self.request.user)


@extend_schema_view(
    list=extend_schema(
            summary="Получение списка моих комментариев",
    ),
    update=extend_schema(
        summary="Изменение моего комментария",
    ),
    create=extend_schema(
            summary="Создание нового комментария",
    ),
    delete=extend_schema(
        summary="Удаление моего комментария"
    )
)
class MyCommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


@extend_schema_view(
    create=extend_schema(
            summary="Регистрация пользователя",
    ),
)
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


@extend_schema(tags=['Looks'])
@extend_schema_view(
    post=extend_schema(
            summary="Поставить/удалить лайк у образа",
    ),
)
class LikeCreateAPIView(APIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        look = get_object_or_404(Look, slug=request.data.get('slug'))
        if request.user not in look.likes.all():
            request.user.likes.add(look)
            return Response({'detail': 'Successfully liked'}, status=status.HTTP_200_OK)
        else:
            request.user.likes.remove(look)
            return Response({'detail': 'Successfully unliked'}, status=status.HTTP_200_OK)

