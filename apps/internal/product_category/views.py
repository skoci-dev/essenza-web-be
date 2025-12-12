from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required, validate_body, jwt_role_required
from core.enums import UserRole
from utils import api_response
from services import ProductCategoryService
from services.product_category import dto
from docs.api.internal import ProductCategoryAPI

from . import serializers


class ProductCategoryViewSet(BaseViewSet):
    """ViewSet for managing product categories."""

    _product_category_service = ProductCategoryService()

    @ProductCategoryAPI.create_product_category_schema
    @jwt_role_required([UserRole.SUPERADMIN, UserRole.ADMIN])
    @validate_body(serializers.PostCreateProductCategoryRequest)
    def create_product_category(self, request: Request, validated_data) -> Response:
        """Create a new product category."""
        product_category_service = ProductCategoryService()
        product_category, error = product_category_service.use_context(
            request
        ).create_product_category(dto.CreateProductCategoryDTO(**validated_data))

        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Product category created successfully.",
            data=serializers.ProductCategoryModelSerializer(product_category).data,
        )

    @ProductCategoryAPI.list_product_categories_schema
    @jwt_required
    def list_product_categories(self, request: Request) -> Response:
        """List product categories with optional filtering."""
        is_active_param = request.query_params.get("is_active")
        is_active = None
        if is_active_param == "true":
            is_active = True
        elif is_active_param == "false":
            is_active = False

        filter_dto = dto.FilterProductCategoryDTO(is_active=is_active)

        product_category_service = ProductCategoryService()
        product_categories = product_category_service.use_context(
            request
        ).get_product_categories(filter_dto)

        serialized_data = serializers.ProductCategoryModelSerializer(
            product_categories, many=True
        ).data

        return api_response(request).success(
            message="Product categories retrieved successfully.",
            data=serialized_data,
        )

    @ProductCategoryAPI.retrieve_product_category_schema
    @jwt_required
    def retrieve_product_category(self, request: Request, slug: str) -> Response:
        """Retrieve a specific product category by ID."""
        product_category_service = ProductCategoryService()
        product_category = product_category_service.use_context(
            request
        ).get_product_category_by_slug(slug)

        if not product_category:
            return api_response(request).error(
                message="Product category not found.", status_code=404
            )

        serialized_data = serializers.ProductCategoryModelSerializer(
            product_category
        ).data

        return api_response(request).success(
            message="Product category retrieved successfully.",
            data=serialized_data,
        )

    @ProductCategoryAPI.update_product_category_schema
    @jwt_role_required([UserRole.SUPERADMIN, UserRole.ADMIN])
    @validate_body(serializers.PutUpdateProductCategoryRequest)
    def update_product_category(
        self, request: Request, slug: str, validated_data
    ) -> Response:
        """Update an existing product category."""
        product_category_service = ProductCategoryService()
        product_category, error = product_category_service.use_context(
            request
        ).update_product_category(slug, dto.CreateProductCategoryDTO(**validated_data))

        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Product category updated successfully.",
            data=serializers.ProductCategoryModelSerializer(product_category).data,
        )

    @ProductCategoryAPI.delete_product_category_schema
    @jwt_role_required([UserRole.SUPERADMIN, UserRole.ADMIN])
    def delete_product_category(self, request: Request, slug: str) -> Response:
        """Delete a specific product category by ID."""
        product_category_service = ProductCategoryService()
        error = product_category_service.use_context(request).delete_product_category(
            slug
        )

        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Product category deleted successfully."
        )
