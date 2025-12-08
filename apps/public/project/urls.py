from django.urls import path

from .views import ProjectPublicViewSet


urlpatterns = [
    path("", ProjectPublicViewSet.as_view({"get": "list_projects"})),
    path("/<slug:slug>", ProjectPublicViewSet.as_view({"get": "retrieve_project"})),
]
