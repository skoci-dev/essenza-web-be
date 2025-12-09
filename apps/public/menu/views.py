from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from utils import api_response
from services import MenuService
from docs.api.public import MenuPublicAPI

from . import serializers


class MenuPublicViewSet(BaseViewSet):
    """Public ViewSet for managing menus."""

    _menu_service = MenuService()

    @MenuPublicAPI.list_menus_schema
    def list_menus(self, request: Request) -> Response:
        """List all menus."""
        menus = MenuPublicViewSet._menu_service.get_menus(tree=True)

        return api_response(request).success(
            message="Menus retrieved successfully.",
            data=serializers.MenuCollectionSerializer(menus, many=True).data,
        )
