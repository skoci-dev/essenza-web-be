from django.urls import path

from .views import StorePublicViewSet


urlpatterns = [path("", StorePublicViewSet.as_view({"get": "list_stores"}))]
