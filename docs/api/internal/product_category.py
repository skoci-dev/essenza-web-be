from functools import wraps
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.internal.product_category import serializers

TAGS = ["Internal / Product Category Master"]


class ProductCategoryAPI:
    """API schema definitions for Product Category endpoints."""

    @staticmethod
    def create_product_category_schema(func):
        """Schema for creating a product category."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_create_product_category",
            summary="Create Product Category",
            description="Create a new product category.",
            request=serializers.PostCreateProductCategoryRequest,
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def list_product_categories_schema(func):
        """Schema for listing product categories."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_list_product_categories",
            summary="List Product Categories",
            description="List product categories with optional filtering.",
            parameters=[
                OpenApiParameter(
                    name="is_active",
                    type=OpenApiTypes.BOOL,
                    description="Filter by active status (true/false)",
                    required=False,
                ),
            ],
            responses=serializers.ProductCategoryModelSerializer(many=True),
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def update_product_category_schema(func):
        """Schema for updating a product category."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_update_product_category",
            summary="Update Product Category",
            description="Update an existing product category.",
            request=serializers.PutUpdateProductCategoryRequest,
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def retrieve_product_category_schema(func):
        """Schema for retrieving a product category."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_retrieve_product_category",
            summary="Retrieve Product Category",
            description="Retrieve a specific product category by slug.",
            responses=serializers.ProductCategoryModelSerializer,
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def delete_product_category_schema(func):
        """Schema for deleting a product category."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_delete_product_category",
            summary="Delete Product Category",
            description="Delete a specific product category by slug.",
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
