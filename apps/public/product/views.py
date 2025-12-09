from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from utils import api_response
from services import ProductService
from services.product import dto
from docs.api.public import ProductPublicAPI

from . import serializers


class ProductPublicViewSet(BaseViewSet):
    """Public ViewSet for managing products."""

    _product_service = ProductService()

    @ProductPublicAPI.list_products_schema
    def list_products(self, request: Request) -> Response:
        """List all products."""
        str_page_number = request.query_params.get("page", "1")
        str_page_size = request.query_params.get("page_size", "20")
        search = request.query_params.get("search", None)

        page = ProductPublicViewSet._product_service.get_paginated_products(
            str_page_number=str_page_number,
            str_page_size=str_page_size,
            filters=dto.ProductFilterDTO(is_active=True, fulltext_search=search),
        )

        return api_response(request).paginated(
            message="Products retrieved successfully.",
            data=serializers.ProductCollectionSerializer(page, many=True).data,
            page=page,
        )

    @ProductPublicAPI.retrieve_product_schema
    def retrieve_product(self, request: Request, slug: str) -> Response:
        """Retrieve a specific product by slug."""
        product, error = ProductPublicViewSet._product_service.get_product_by_slug(
            slug=slug
        )
        if error:
            return api_response(request).error(
                message=str(error),
            )

        return api_response(request).success(
            message="Product retrieved successfully.",
            data=serializers.ProductDetailSerializer(product).data,
        )
