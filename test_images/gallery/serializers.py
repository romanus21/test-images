from rest_framework.serializers import ModelSerializer

from gallery.models import Image


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ["image", "owner", "id", "title"]
        read_only_fields = ["owner", "id"]
