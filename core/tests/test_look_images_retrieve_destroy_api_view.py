import os
import shutil

from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from django.test import override_settings

from LookBook.settings import BASE_DIR
from core.models import User, Look, LookImages
from core.tests.utils import generate_image_bytes
from django.core.files import File


TEST_DIR = os.path.join(BASE_DIR, 'test_media')


@override_settings(MEDIA_ROOT=TEST_DIR)
class LookImagesRetrieveDestroyAPIViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email="test_user@gmail.com", username="TestUser",
                                       password="TestUserPassword")
        cls.user_look = Look.objects.create(name='test look 1', description='test 1',
                                            gender='ml', slug='test-look-1', author=cls.user)
        cls.another_user = User.objects.create(email="another_user@gmail.com", username="AnotherUser",
                                               password="AnotherUserPassword")
        cls.image = LookImages.objects.create(image=File(generate_image_bytes(cls)), look=cls.user_look)

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        print
        "\nDeleting temporary files...\n"
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass

    def test_user_can_delete_image(self):
        self.client.force_authenticate(self.user)
        slug = self.user_look.slug
        response = self.client.delete(path=reverse('image-detail',
                                                 kwargs={'look_slug': slug, 'pk': self.image.pk}))
        look = Look.objects.get(slug=slug)
        deleted_image = LookImages.objects.filter(look=look)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(deleted_image, msg='look is not deleted')

    def test_another_user_cant_delete_image(self):
        self.client.force_authenticate(self.another_user)
        slug = self.user_look.slug
        response = self.client.delete(path=reverse('image-detail',
                                                   kwargs={'look_slug': slug, 'pk': self.image.pk}))
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_cant_delete_image(self):
        slug = self.user_look.slug
        response = self.client.delete(path=reverse('image-detail',
                                                   kwargs={'look_slug': slug, 'pk': self.image.pk}))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

