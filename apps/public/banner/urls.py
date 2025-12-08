from django.urls import path

from .views import BannerPublicViewSet


urlpatterns = [path("", BannerPublicViewSet.as_view({"get": "list_banners"}))]
