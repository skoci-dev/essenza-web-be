from django.urls import path

from .views import SettingPublicViewSet


urlpatterns = [
    path(
        "", SettingPublicViewSet.as_view({"get": "list_settings"}), name="list-settings"
    ),
    path(
        "/<slug:slug>",
        SettingPublicViewSet.as_view({"get": "retrieve_setting"}),
        name="retrieve-setting",
    ),
]
