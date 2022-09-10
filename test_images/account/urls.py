from django.conf.urls import handler404, handler500  # noqa
from django.urls import include, path

from account.views.Me import MeAPIView
from account.views.Register import RegisterViewSet

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("me/", MeAPIView.as_view()),
    path("register/", RegisterViewSet.as_view()),
]
