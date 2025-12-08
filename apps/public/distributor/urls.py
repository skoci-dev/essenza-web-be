from django.urls import path

from .views import DistributorPublicViewSet


urlpatterns = [path("", DistributorPublicViewSet.as_view({"get": "list_distributors"}))]
