from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from gallery.serializers import ImageSerializer


class ImagesViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return self.request.user.images.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
