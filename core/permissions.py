from rest_framework import permissions
from rest_framework.permissions import BasePermission

from core.models import Look, Clothes


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user == obj.author


class NestedIsAuthorOrReadOnly(BasePermission):
    model = None
    foreign_field = None
    slug = None

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        atr = getattr(obj, self.foreign_field)
        return request.user == atr.author

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        obj = self.model.objects.get(slug=view.kwargs[self.slug])
        return obj.author == request.user


class LookIsAuthorOrReadOnly(NestedIsAuthorOrReadOnly):
    model = Look
    foreign_field = 'look'
    slug = 'look_slug'


class ClothesIsAuthorOrReadOnly(NestedIsAuthorOrReadOnly):
    model = Clothes
    foreign_field = 'clothes'
    slug = 'clothes_slug'
