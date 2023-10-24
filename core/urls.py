from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReadOnlyLooksViewSet, ReadOnlyClothesViewSet, MyLooksViewSet, MyClothesViewSet, ImageCreateAPIView, \
    LookImagesRetrieveDestroyAPIView, MyCommentsViewSet, RegistrationUserView, \
    LikeCreateAPIView, update_server

router = DefaultRouter()
router.register('looks', ReadOnlyLooksViewSet, basename='looks')
router.register('clothes', ReadOnlyClothesViewSet, basename='clothes')
router.register('my_looks', MyLooksViewSet, basename='my_looks')
router.register('my_clothes', MyClothesViewSet, basename='my_clothes')
router.register('my_comments', MyCommentsViewSet, basename='my_comments')


urlpatterns = [
    path("", include(router.urls)),
    path("like_look/", LikeCreateAPIView.as_view(), name='like_look'),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
    path('my_looks/<slug:look_slug>/add_image/', ImageCreateAPIView.as_view()),
    path('my_looks/<slug:look_slug>/image/<int:pk>', LookImagesRetrieveDestroyAPIView.as_view()),
]
