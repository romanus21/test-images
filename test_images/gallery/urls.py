from django.urls import path
from rest_framework.routers import DefaultRouter

from gallery.views.AdminImages import AdminImagesView
from gallery.views.Images import ImagesViewSet

router = DefaultRouter()
router.register(r"images", ImagesViewSet, basename="image")

urlpatterns = [path("admin/images/", AdminImagesView.as_view())] + router.urls
