from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from gallery.models import Image


class AdminImagesView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request):
        images = Image.objects.all()
        if images:
            images.delete()
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)
