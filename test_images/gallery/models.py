from django.contrib.auth.models import User
from django.db import models


class Image(models.Model):
    upload_to = "gallery/"

    title = models.CharField(null=True, blank=True, max_length=100)
    image = models.ImageField(
        upload_to=upload_to,
        null=False,
        blank=False,
    )
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="images",
        null=False,
        blank=False,
    )
