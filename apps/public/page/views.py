from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from utils import api_response
from services import PageService
from services.page import dto
from docs.api.public import PagePublicAPI

from . import serializers


class PagePublicViewSet(BaseViewSet):
    """Public ViewSet for managing pages."""

    _page_service = PageService()

    @PagePublicAPI.list_pages_schema
    def list_pages(self, request: Request) -> Response:
        """List all pages."""
        str_page_number = request.query_params.get("page", "1")
        str_page_size = request.query_params.get("page_size", "20")

        page = PagePublicViewSet._page_service.get_paginated_pages(
            str_page_number=str_page_number,
            str_page_size=str_page_size,
            filters=dto.PageFilterDTO(is_active=True),
        )

        return api_response(request).paginated(
            message="Pages retrieved successfully.",
            data=serializers.PageCollectionSerializer(page, many=True).data,
            page=page,
        )

    @PagePublicAPI.retrieve_page_schema
    def retrieve_page(self, request: Request, slug: str) -> Response:
        """Retrieve a specific page by slug."""
        page, error = PagePublicViewSet._page_service.get_page_by_slug(slug=slug)
        if error:
            return api_response(request).error(
                message=str(error),
            )

        return api_response(request).success(
            message="Page retrieved successfully.",
            data=serializers.PageDetailSerializer(page).data,
        )
