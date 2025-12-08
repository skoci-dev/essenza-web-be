from django.urls import path

from .views import SocialMediaPublicViewSet


urlpatterns = [path("", SocialMediaPublicViewSet.as_view({"get": "list_social_media"}))]
