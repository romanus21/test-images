import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from gallery.models import Image

test_path = os.path.join(settings.BASE_DIR, "gallery/data/test")


@override_settings(MEDIA_ROOT=os.path.join(test_path, "media"))
class AdminImagesTest(TestCase):
    image_path = os.path.join(
        settings.BASE_DIR, "gallery/data/test/test_image.jpg"
    )

    creds = {"username": "test", "password": "test"}

    url = "/api/v1/gallery/admin/images/"

    def test_non_auth_and_not_admin(self):
        client = APIClient()
        response = client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user = User.objects.create_user(**self.creds)
        user.save()

        client.login(**self.creds)
        response = client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_with_admin(self):
        superuser = User.objects.create_superuser(**self.creds)
        superuser.save()
        client = APIClient()
        client.login(**self.creds)
        response = client.delete(self.url)
        self.assertEqual(response.status_code, 400)

        uploaded_image = SimpleUploadedFile(
            name="test_image.jpg",
            content=open(self.image_path, "rb").read(),
            content_type="image/jpeg",
        )

        Image.objects.create(
            image=uploaded_image, owner=superuser, title="Тест"
        )

        Image.objects.create(
            image=uploaded_image, owner=superuser, title="Тест1"
        )

        response = client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Image.objects.all().count(), 0)

    @classmethod
    def tearDownClass(cls):
        media_gallery_path = os.path.join(test_path, "media/gallery")
        for path in os.listdir(media_gallery_path):
            os.remove(os.path.join(media_gallery_path, path))
