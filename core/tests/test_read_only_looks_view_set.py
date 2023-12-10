from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from rest_framework import status

from core.models import Look, User
from core.serializers import LookSerializer

client = APIClient()


class ReadOnlyLooksViewSetTest(TestCase):



    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email="test_user@gmail.com", username="TestUser",
                                   password="TestUserPassword")
        cls.test1 = Look.objects.create(name='test look 1', description='test 1',
                                        gender='ml', slug='test-look-1', author=user)
        cls.test2 = Look.objects.create(name='test look 2', description='test 2',
                                        gender='ml', slug='test-look-2', author=user)

    def test_user_can_get_look_list(self):
        response = client.get(reverse('looks-list'))
        looks = Look.objects.all()
        serializer = LookSerializer(looks, many=True)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_can_get_look_detail(self):
        test_slug = self.test1.slug
        response = client.get(reverse('looks-detail', args=[test_slug]))
        look = Look.objects.get(slug=test_slug)
        serializer = LookSerializer(look)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_puppy(self):
        fail_slug = '123'
        response = client.get(
            reverse('looks-detail', args=[fail_slug]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)






