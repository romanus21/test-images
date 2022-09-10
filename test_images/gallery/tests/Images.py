import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

test_path = os.path.join(settings.BASE_DIR, "gallery/data/test")


@override_settings(MEDIA_ROOT=os.path.join(test_path, "media"))
class ImagesTest(TestCase):
    image_path = os.path.join(
        settings.BASE_DIR, "gallery/data/test/test_image.jpg"
    )

    creds = {"username": "test", "password": "test"}

    url = "/api/v1/gallery/images/"

    def test_non_auth(self):
        client = APIClient()
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_with_auth(self):
        user = User.objects.create_user(**self.creds)
        user.save()
        client = APIClient()
        client.login(**self.creds)
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.data, [])

        uploaded_image = SimpleUploadedFile(
            name="test_image.jpg",
            content=open(self.image_path, "rb").read(),
            content_type="image/jpeg",
        )

        response = client.post(
            self.url, {"image": uploaded_image, "title": "Тест"}
        )

        self.assertEqual(user.images.all().count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.images.first().title, "Тест")
        self.assertEqual(
            user.images.first().image.name, "gallery/test_image.jpg"
        )

        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data[0]["image"],
            "http://testserver/media/gallery/test_image.jpg",
        )
        self.assertEqual(response.data[0]["owner"], 1)

        response = client.patch(self.url + "1/", {"title": "Новый тест"})

        self.assertEqual(user.images.first().title, "Новый тест")
        self.assertEqual(response.status_code, 200)
        response = client.get(self.url)
        self.assertEqual(
            response.data[0]["image"],
            "http://testserver/media/gallery/test_image.jpg",
        )
        self.assertEqual(response.data[0]["owner"], 1)
        self.assertEqual(response.data[0]["title"], "Новый тест")

        response = client.delete(self.url + "1/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(user.images.all().count(), 0)

    @classmethod
    def tearDownClass(cls):
        media_gallery_path = os.path.join(test_path, "media/gallery")
        for path in os.listdir(media_gallery_path):
            os.remove(os.path.join(media_gallery_path, path))
