from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from utils import api_response
from services import SettingService
from services.setting import dto
from docs.api.public import SettingPublicAPI

from . import serializers


class SettingPublicViewSet(BaseViewSet):
    """Public ViewSet for managing application settings."""

    _setting_service = SettingService()

    @SettingPublicAPI.list_settings_schema
    def list_settings(self, request: Request) -> Response:
        """List all application settings."""
        settings = SettingService().get_all_settings(
            dto.FilterSettingsDTO(is_active=True)
        )

        return api_response(request).success(
            message="Settings retrieved successfully.",
            data=serializers.SettingCollectionSerializer(settings, many=True).data,
        )

    @SettingPublicAPI.retrieve_setting_schema
    def retrieve_setting(self, request: Request, slug: str) -> Response:
        """Retrieve a specific setting by its slug."""
        setting = SettingService().get_setting_by_slug(slug)

        if not setting:
            return api_response(request).error(
                message=f"Setting with slug '{slug}' not found."
            )

        serialized_setting = serializers.SettingCollectionSerializer(setting).data

        return api_response(request).success(
            message="Setting retrieved successfully.",
            data=serialized_setting,
        )
