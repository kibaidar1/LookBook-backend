from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReadOnlyLooksViewSet, ReadOnlyClothesViewSet

router = DefaultRouter()
router.register('looks', ReadOnlyLooksViewSet, basename='looks')
router.register('clothes', ReadOnlyClothesViewSet, basename='clothes')


urlpatterns = [
    path("", include(router.urls)),
]
