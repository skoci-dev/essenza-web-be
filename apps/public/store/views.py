from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from utils import api_response
from services import StoreService
from docs.api.public import StorePublicAPI

from . import serializers


class StorePublicViewSet(BaseViewSet):
    """Public ViewSet for managing store locations."""

    _store_service = StoreService()

    @StorePublicAPI.list_stores_schema
    def list_stores(self, request: Request) -> Response:
        """List all store locations."""
        str_page_number = request.query_params.get("page", "1")
        str_page_size = request.query_params.get("page_size", "20")

        page = StorePublicViewSet._store_service.get_paginated_stores(
            str_page_number=str_page_number,
            str_page_size=str_page_size,
        )

        return api_response(request).paginated(
            message="Store locations retrieved successfully.",
            data=serializers.StoreCollectionSerializer(page, many=True).data,
            page=page,
        )
