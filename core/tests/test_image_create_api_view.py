import os
import shutil

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import override_settings

from LookBook.settings import BASE_DIR
from core.models import User, Look, LookImages
from core.tests.utils import generate_image_bytes

TEST_DIR = os.path.join(BASE_DIR, 'test_media')


@override_settings(MEDIA_ROOT=TEST_DIR)
class ImageCreateAPIViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email="test_user@gmail.com", username="TestUser",
                                       password="TestUserPassword")
        cls.user_look = Look.objects.create(name='test look 1', description='test 1',
                                            gender='ml', slug='test-look-1', author=cls.user)
        cls.another_user = User.objects.create(email="another_user@gmail.com", username="AnotherUser",
                                               password="AnotherUserPassword")

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        print
        "\nDeleting temporary files...\n"
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass

    def test_user_can_add_valid_image_to_look(self):
        self.client.force_authenticate(self.user)
        slug = self.user_look.slug
        image_file = generate_image_bytes(self)
        response = self.client.post(path=reverse('image-post', kwargs={'look_slug': slug}),
                                    data={'image': image_file},
                                    format='multipart')
        look = Look.objects.get(slug=slug)
        look_image = LookImages.objects.get(look=look)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(look_image)

    def test_user_cant_add_invalid_image_to_look(self):
        self.client.force_authenticate(self.user)
        slug = self.user_look.slug
        response = self.client.post(path=reverse('image-post', kwargs={'look_slug': slug}),
                                    data={'image': generate_image_bytes(self, file_extension='pdf')},
                                    format='multipart')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_another_user_cant_add_image_to_look(self):
        self.client.force_authenticate(self.another_user)
        slug = self.user_look.slug
        response = self.client.post(path=reverse('image-post', kwargs={'look_slug': slug}),
                                    data={'image': generate_image_bytes(self)},
                                    format='multipart')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_user_cant_add_image_to_look(self):
        slug = self.user_look.slug
        response = self.client.post(path=reverse('image-post', kwargs={'look_slug': slug}),
                                    data={'image': generate_image_bytes(self)},
                                    format='multipart')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


