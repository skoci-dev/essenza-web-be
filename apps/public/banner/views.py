from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from utils import api_response
from services import BannerService
from services.banner import dto
from docs.api.public import BannerPublicAPI

from . import serializers


class BannerPublicViewSet(BaseViewSet):
    """Public ViewSet for managing banner links."""

    _banner_service = BannerService()

    @BannerPublicAPI.list_banner_schema
    def list_banners(self, request: Request) -> Response:
        """List all banner links."""
        str_page_number = request.query_params.get("page", "1")
        str_page_size = request.query_params.get("page_size", "20")

        page = self._banner_service.get_paginated_banners(
            str_page_number=str_page_number,
            str_page_size=str_page_size,
            filters=dto.BannerFilterDTO(is_active=True),
        )

        return api_response(request).paginated(
            message="Banner links retrieved successfully.",
            data=serializers.BannerCollectionSerializer(page, many=True).data,
            page=page,
        )
