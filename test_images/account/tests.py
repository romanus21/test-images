import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from gallery.models import Image

test_path = os.path.join(settings.BASE_DIR, "account/data/test")


@override_settings(MEDIA_ROOT=os.path.join(test_path, "media"))
class MeAPIVIewTest(TestCase):
    image_path = os.path.join(
        settings.BASE_DIR, "account/data/test/test_image.jpg"
    )

    def test_non_auth(self):
        client = APIClient()
        response = client.get("/api/v1/account/me/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_with_auth(self):
        creds = {"username": "test", "password": "test"}
        user = User.objects.create_user(**creds)
        user.save()
        client = APIClient()
        client.login(**creds)
        response = client.get("/api/v1/account/me/")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data.get("username"), user.username)

        self.assertListEqual(response.data.get("images"), [])

        uploaded_image = SimpleUploadedFile(
            name="test_image.jpg",
            content=open(self.image_path, "rb").read(),
            content_type="image/jpeg",
        )

        Image.objects.create(image=uploaded_image, owner=user, title="Тест")

        response = client.get("/api/v1/account/me/")

        image = response.data.get("images")[0]

        self.assertEqual(image["id"], 1)
        self.assertEqual(image["title"], "Тест")
        self.assertEqual(image["image"], "/media/gallery/test_image.jpg")

    @classmethod
    def tearDownClass(cls):
        media_gallery_path = os.path.join(test_path, "media/gallery")
        for path in os.listdir(media_gallery_path):
            os.remove(os.path.join(media_gallery_path, path))


class TestRegister(TestCase):
    def test_register_and_login(self):
        client = APIClient()
        creds = {"username": "test_username", "password": "test_password"}
        response = client.post("/api/v1/account/register/", creds)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get("/api/v1/account/me/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client.login(**creds)
        response = client.get("/api/v1/account/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
