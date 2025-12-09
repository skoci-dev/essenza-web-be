from django.urls import path

from .views import PagePublicViewSet


urlpatterns = [
    path("", PagePublicViewSet.as_view({"get": "list_pages"})),
    path("/<slug:slug>", PagePublicViewSet.as_view({"get": "retrieve_page"})),
]
