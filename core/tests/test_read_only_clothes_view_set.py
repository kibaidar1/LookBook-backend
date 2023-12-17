from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from rest_framework import status

from core.models import User, Clothes
from core.serializers import ClothesSerializer

client = APIClient()


class ReadOnlyClothesViewSetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email="test_user@gmail.com", username="TestUser",
                                   password="TestUserPassword")
        cls.test1 = Clothes.objects.create(name='test clothes 1', gender='ml',
                                           slug='test-clothes-1', author=user)
        cls.test2 = Clothes.objects.create(name='test clothes 2', gender='ml',
                                           slug='test-clothes-2', author=user)

    def test_user_can_get_clothes_list(self):
        response = client.get(reverse('clothes-list'))
        looks = Clothes.objects.all()
        serializer = ClothesSerializer(looks, many=True)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_can_get_clothes_detail(self):
        test_slug = self.test1.slug
        response = client.get(reverse('clothes-detail', args=[test_slug]))
        look = Clothes.objects.get(slug=test_slug)
        serializer = ClothesSerializer(look)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_puppy(self):
        fail_slug = '123'
        response = client.get(
            reverse('clothes-detail', args=[fail_slug]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

