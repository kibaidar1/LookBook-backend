import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from rest_framework import status

from core.models import Look, User
from core.serializers import LookSerializer


class MyLooksViewSetTest(TestCase):
    valid_payload = {
        'name': 'test look',
        'description': 'test',
        'gender': 'ml',
        'slug': 'test-look'
    }
    invalid_payload = {
        'name': '',
        'description': 'test',
        'gender': 'ml',
        'slug': 'test-look'
    }

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(email="test_user@gmail.com", username="TestUser",
                                            password="TestUserPassword")
        cls.test_user_look = Look.objects.create(name='test look 1', description='test 1',
                                                 gender='ml', slug='test-look-1', author=cls.test_user)
        cls.another_user = User.objects.create(email="another_user@gmail.com", username="AnotherUser",
                                               password="AnotherUserPassword")

    def setUp(self):
        self.client = APIClient()

    def test_user_can_get_his_looks(self):
        user = self.test_user
        self.client.force_authenticate(user)
        response = self.client.get(reverse('my_looks-list'))
        looks = Look.objects.filter(author=user)
        serializer = LookSerializer(looks, many=True)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_can_get_look_detail(self):
        user = self.test_user
        self.client.force_authenticate(user)
        slug = self.test_user_look.slug
        response = self.client.get(reverse('looks-detail', args=[slug]))
        look = Look.objects.get(slug=slug)
        serializer = LookSerializer(look)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_can_post_valid_look(self):
        user = self.test_user
        self.client.force_authenticate(user)
        response = self.client.post(reverse('my_looks-list'),
                                    data=json.dumps(self.valid_payload),
                                    content_type='application/json')
        created_look = Look.objects.get(slug=self.valid_payload['slug'])
        serializer = LookSerializer(created_look)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data, serializer.data)

    def test_user_cant_post_invalid_look(self):
        user = self.test_user
        self.client.force_authenticate(user)
        response = self.client.post(reverse('my_looks-list'),
                                    data=json.dumps(self.invalid_payload),
                                    content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_user_cant_post_look(self):
        response = self.client.post(reverse('my_looks-list'),
                                    data=json.dumps(self.valid_payload),
                                    content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_valid_update_look(self):
        user = self.test_user
        self.client.force_authenticate(user)
        slug = self.test_user_look.slug
        response = self.client.put(reverse('my_looks-detail', args=[slug]),
                                   data=json.dumps(self.valid_payload),
                                   content_type='application/json')
        updated_look = Look.objects.get(slug=self.valid_payload['slug'])
        serializer = LookSerializer(updated_look)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_user_cant_invalid_update_look(self):
        user = self.test_user
        self.client.force_authenticate(user)
        slug = self.test_user_look.slug
        response = self.client.put(reverse('my_looks-detail', args=[slug]),
                                   data=json.dumps(self.invalid_payload),
                                   content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_another_user_cant_update_look(self):
        self.client.force_authenticate(self.another_user)
        slug = self.test_user_look.slug
        response = self.client.put(reverse('my_looks-detail', args=[slug]),
                                   data=json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_user_cant_update_look(self):
        slug = self.test_user_look.slug
        response = self.client.put(reverse('my_looks-detail', args=[slug]),
                                   data=json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_delete_look(self):
        user = self.test_user
        self.client.force_authenticate(user)
        slug = self.test_user_look.slug
        response = self.client.delete(reverse('my_looks-detail', args=[slug]))
        deleted_look = Look.objects.filter(slug=slug) or False
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(deleted_look, msg='look is not deleted')

    def test_another_user_cant_delete_look(self):
        self.client.force_authenticate(self.another_user)
        slug = self.test_user_look.slug
        response = self.client.delete(reverse('my_looks-detail', args=[slug]))
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_user_cant_delete_look(self):
        slug = self.test_user_look.slug
        response = self.client.delete(reverse('my_looks-detail', args=[slug]))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
