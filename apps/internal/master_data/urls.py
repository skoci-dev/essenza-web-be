from django.urls import path

from .views import MasterDataViewSet


urlpatterns = [
    path(
        "/cities",
        MasterDataViewSet.as_view({"get": "get_all_cities"}),
        name="get_all_cities",
    ),
]
