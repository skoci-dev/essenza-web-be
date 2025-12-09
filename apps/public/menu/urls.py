from django.urls import path

from .views import MenuPublicViewSet


urlpatterns = [path("", MenuPublicViewSet.as_view({"get": "list_menus"}))]
