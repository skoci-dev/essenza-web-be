"""
Product API Documentation Schema
Contains OpenAPI/Swagger documentation for all product endpoints
"""

from functools import wraps
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.internal.product import serializers
from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Internal / Product"]


class ProductAPI:
    """API schema definitions for Product endpoints."""

    @staticmethod
    def create_product_schema(func):
        """Schema for creating a new product."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_create_product",
            summary="Create Product",
            description="Create a new product with file upload support.",
            request={"multipart/form-data": serializers.PostCreateProductRequest},
            responses={
                200: {
                    "description": "Product created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product created successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "ceramic-tile-floor-01",
                                },
                                "name": {
                                    "type": "string",
                                    "example": "Premium Ceramic Floor Tile",
                                },
                                "lang": {"type": "string", "example": "en"},
                                "model": {"type": "string", "example": "CT-FL-001"},
                                "size": {"type": "string", "example": "60x60 cm"},
                                "description": {
                                    "type": "string",
                                    "example": "High-quality ceramic floor tile suitable for residential and commercial use.",
                                },
                                "product_type": {"type": "string", "example": "lantai"},
                                "image": {
                                    "type": "string",
                                    "format": "uri",
                                    "example": "/media/uploads/products/ceramic-tile-floor-01_main.jpg",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string", "format": "uri"},
                                    "example": [
                                        "/media/uploads/products/gallery/ceramic-tile-floor-01_gallery_0.jpg",
                                        "/media/uploads/products/gallery/ceramic-tile-floor-01_gallery_1.jpg",
                                    ],
                                },
                                "brochure": {
                                    "type": "object",
                                    "nullable": True,
                                    "properties": {
                                        "id": {"type": "integer", "example": 1},
                                        "title": {
                                            "type": "string",
                                            "example": "Product Brochure",
                                        },
                                        "file_url": {
                                            "type": "string",
                                            "format": "uri",
                                            "example": "/media/brochures/product-brochure.pdf",
                                        },
                                    },
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "Premium Ceramic Floor Tile - High Quality",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "High-quality ceramic floor tile suitable for residential and commercial use. Available in multiple sizes and finishes.",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "ceramic, tile, floor, premium, lantai",
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Validation error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Product with this slug already exists.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def get_products_schema(func):
        """Schema for retrieving all products with filtering."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_get_products",
            summary="Retrieve all products",
            description="Retrieve all products with optional filtering by type, language, and search.",
            parameters=[
                *DEFAULT_PAGINATION_PARAMS,
                OpenApiParameter(
                    name="type",
                    description="Filter by product type",
                    required=False,
                    type=OpenApiTypes.STR,
                    enum=["lantai", "dinding"],
                ),
                OpenApiParameter(
                    name="search",
                    description="Search in name, description, and model",
                    required=False,
                    type=OpenApiTypes.STR,
                ),
                OpenApiParameter(
                    name="is_active",
                    description="Filter by active status",
                    required=False,
                    type=OpenApiTypes.BOOL,
                ),
            ],
            responses={
                200: {
                    "description": "Products retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Products retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "slug": {
                                        "type": "string",
                                        "example": "ceramic-tile-floor-01",
                                    },
                                    "name": {
                                        "type": "string",
                                        "example": "Premium Ceramic Floor Tile",
                                    },
                                    "lang": {"type": "string", "example": "en"},
                                    "model": {"type": "string", "example": "CT-FL-001"},
                                    "size": {"type": "string", "example": "60x60 cm"},
                                    "description": {
                                        "type": "string",
                                        "example": "High-quality ceramic floor tile suitable for residential and commercial use.",
                                    },
                                    "product_type": {
                                        "type": "string",
                                        "example": "lantai",
                                    },
                                    "image": {
                                        "type": "string",
                                        "format": "uri",
                                        "example": "/media/uploads/products/ceramic-tile-floor-01_main.jpg",
                                    },
                                    "gallery": {
                                        "type": "array",
                                        "items": {"type": "string", "format": "uri"},
                                        "example": [
                                            "/media/uploads/products/gallery/ceramic-tile-floor-01_gallery_0.jpg"
                                        ],
                                    },
                                    "brochure": {
                                        "type": "object",
                                        "nullable": True,
                                        "properties": {
                                            "id": {"type": "integer", "example": 1},
                                            "title": {
                                                "type": "string",
                                                "example": "Product Brochure",
                                            },
                                            "file_url": {
                                                "type": "string",
                                                "format": "uri",
                                                "example": "/media/brochures/product-brochure.pdf",
                                            },
                                        },
                                    },
                                    "meta_title": {
                                        "type": "string",
                                        "example": "Premium Ceramic Floor Tile - High Quality",
                                    },
                                    "meta_description": {
                                        "type": "string",
                                        "example": "High-quality ceramic floor tile suitable for residential and commercial use.",
                                    },
                                    "meta_keywords": {
                                        "type": "string",
                                        "example": "ceramic, tile, floor, premium",
                                    },
                                    "is_active": {"type": "boolean", "example": True},
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-28T10:30:00.000000+07:00",
                                    },
                                    "updated_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-28T10:30:00.000000+07:00",
                                    },
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000",
                                },
                                "pagination": {
                                    "type": "object",
                                    "properties": {
                                        "current_page": {
                                            "type": "integer",
                                            "example": 1,
                                        },
                                        "per_page": {"type": "integer", "example": 20},
                                        "total_pages": {
                                            "type": "integer",
                                            "example": 5,
                                        },
                                        "total_items": {
                                            "type": "integer",
                                            "example": 95,
                                        },
                                        "has_next": {
                                            "type": "boolean",
                                            "example": True,
                                        },
                                        "has_previous": {
                                            "type": "boolean",
                                            "example": False,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def get_specific_product_schema(func):
        """Schema for retrieving a specific product by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_get_specific_product",
            summary="Retrieve a specific product by ID",
            description="Retrieve a specific product by its ID.",
            responses={
                200: {
                    "description": "Product retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "ceramic-tile-floor-01",
                                },
                                "name": {
                                    "type": "string",
                                    "example": "Premium Ceramic Floor Tile",
                                },
                                "lang": {"type": "string", "example": "en"},
                                "model": {"type": "string", "example": "CT-FL-001"},
                                "size": {"type": "string", "example": "60x60 cm"},
                                "description": {
                                    "type": "string",
                                    "example": "High-quality ceramic floor tile suitable for residential and commercial use. Features excellent durability and water resistance.",
                                },
                                "product_type": {"type": "string", "example": "lantai"},
                                "image": {
                                    "type": "string",
                                    "format": "uri",
                                    "example": "/media/uploads/products/ceramic-tile-floor-01_main.jpg",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string", "format": "uri"},
                                    "example": [
                                        "/media/uploads/products/gallery/ceramic-tile-floor-01_gallery_0.jpg",
                                        "/media/uploads/products/gallery/ceramic-tile-floor-01_gallery_1.jpg",
                                    ],
                                },
                                "brochure": {
                                    "type": "object",
                                    "nullable": True,
                                    "properties": {
                                        "id": {"type": "integer", "example": 1},
                                        "title": {
                                            "type": "string",
                                            "example": "Premium Ceramic Floor Tile Brochure",
                                        },
                                        "file_url": {
                                            "type": "string",
                                            "format": "uri",
                                            "example": "/media/brochures/ceramic-tile-floor-brochure.pdf",
                                        },
                                    },
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "Premium Ceramic Floor Tile - High Quality Flooring Solution",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Discover our premium ceramic floor tiles. Perfect for residential and commercial spaces with excellent durability and modern design.",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "ceramic tile, floor tile, premium flooring, lantai keramik, durable tiles",
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:35:22.125000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:35:22.130000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Product not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Product with id '99' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:35:22.130000",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def get_product_by_slug_schema(func):
        """Schema for retrieving a product by slug."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_get_product_by_slug",
            summary="Retrieve product by slug",
            description="Retrieve a product by its slug.",
            responses={
                200: {
                    "description": "Product retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "ceramic-tile-floor-01",
                                },
                                "name": {
                                    "type": "string",
                                    "example": "Premium Ceramic Floor Tile",
                                },
                                "lang": {"type": "string", "example": "en"},
                                "model": {"type": "string", "example": "CT-FL-001"},
                                "size": {"type": "string", "example": "60x60 cm"},
                                "description": {
                                    "type": "string",
                                    "example": "High-quality ceramic floor tile suitable for residential and commercial use.",
                                },
                                "product_type": {"type": "string", "example": "lantai"},
                                "image": {
                                    "type": "string",
                                    "format": "uri",
                                    "example": "/media/uploads/products/ceramic-tile-floor-01_main.jpg",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string", "format": "uri"},
                                    "example": [
                                        "/media/uploads/products/gallery/ceramic-tile-floor-01_gallery_0.jpg"
                                    ],
                                },
                                "brochure": {
                                    "type": "object",
                                    "nullable": True,
                                    "properties": {
                                        "id": {"type": "integer", "example": 1},
                                        "title": {
                                            "type": "string",
                                            "example": "Premium Ceramic Floor Tile Brochure",
                                        },
                                        "file_url": {
                                            "type": "string",
                                            "format": "uri",
                                            "example": "/media/brochures/ceramic-tile-floor-brochure.pdf",
                                        },
                                    },
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "Premium Ceramic Floor Tile",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "High-quality ceramic floor tile suitable for residential and commercial use.",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "ceramic tile, floor tile, premium flooring",
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:35:30.245000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Product not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Product with slug 'non-existent' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:35:30.245000",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def update_specific_product_schema(func):
        """Schema for updating a specific product by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_update_specific_product",
            summary="Update a specific product by ID",
            description="Update a specific product by its ID.",
            request={"multipart/form-data": serializers.PutUpdateProductRequest},
            responses={
                200: {
                    "description": "Product updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "ceramic-tile-floor-01-updated",
                                },
                                "name": {
                                    "type": "string",
                                    "example": "Updated Premium Ceramic Floor Tile",
                                },
                                "lang": {"type": "string", "example": "en"},
                                "model": {"type": "string", "example": "CT-FL-001-UPD"},
                                "size": {"type": "string", "example": "80x80 cm"},
                                "description": {
                                    "type": "string",
                                    "example": "Updated high-quality ceramic floor tile with enhanced durability.",
                                },
                                "product_type": {"type": "string", "example": "lantai"},
                                "image": {
                                    "type": "string",
                                    "format": "uri",
                                    "example": "/media/uploads/products/ceramic-tile-floor-01-updated_main.jpg",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string", "format": "uri"},
                                    "example": [
                                        "/media/uploads/products/gallery/ceramic-tile-floor-01_gallery_0.jpg",
                                        "/media/uploads/products/gallery/ceramic-tile-floor-01_gallery_1.jpg",
                                    ],
                                },
                                "brochure": {
                                    "type": "object",
                                    "nullable": True,
                                    "properties": {
                                        "id": {"type": "integer", "example": 1},
                                        "title": {
                                            "type": "string",
                                            "example": "Updated Product Brochure",
                                        },
                                        "file_url": {
                                            "type": "string",
                                            "format": "uri",
                                            "example": "/media/brochures/updated-ceramic-tile-floor-brochure.pdf",
                                        },
                                    },
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "Updated Premium Ceramic Floor Tile",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Enhanced ceramic floor tile with improved features.",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "updated ceramic tile, premium flooring, enhanced durability",
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:45:30.125000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:45:30.130000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Product not found or validation error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Product with id '99' does not exist.",
                        },
                        "errors": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "example": ["This field is required."],
                                },
                                "product_type": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "example": [
                                        "Select a valid choice. invalid_type is not one of the available choices."
                                    ],
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:45:30.130000",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def delete_specific_product_schema(func):
        """Schema for deleting a specific product by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_delete_specific_product",
            summary="Delete a specific product by ID",
            description="Delete a specific product by its ID.",
            responses={
                200: {
                    "description": "Product deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product deleted successfully.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T12:15:45.250000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Product not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Product with id '99' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T12:15:45.250000",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def toggle_product_status_schema(func):
        """Schema for toggling product active status."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_toggle_product_status",
            summary="Toggle product active status",
            description="Toggle product active status by its ID.",
            request=serializers.PatchToggleProductStatusRequest,
            responses={
                200: {
                    "description": "Product status updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product status updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "ceramic-tile-floor-01",
                                },
                                "name": {
                                    "type": "string",
                                    "example": "Premium Ceramic Floor Tile",
                                },
                                "product_type": {"type": "string", "example": "lantai"},
                                "is_active": {"type": "boolean", "example": False},
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T13:20:15.500000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T13:20:15.505000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Product not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Product with id '99' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T13:20:15.505000",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def upload_product_image_schema(func):
        """Schema for uploading product main image."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_upload_product_image",
            summary="Upload product main image",
            description="Upload main image for a specific product.",
            request={"multipart/form-data": serializers.PostUploadProductImageRequest},
            responses={
                200: {
                    "description": "Product image uploaded successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product image uploaded successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "ceramic-tile-floor-01",
                                },
                                "name": {
                                    "type": "string",
                                    "example": "Premium Ceramic Floor Tile",
                                },
                                "image": {
                                    "type": "string",
                                    "format": "uri",
                                    "example": "/media/uploads/products/ceramic-tile-floor-01_main.jpg",
                                },
                                "product_type": {"type": "string", "example": "lantai"},
                                "is_active": {"type": "boolean", "example": True},
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T14:10:35.200000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T14:10:35.205000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Invalid file or product not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Invalid file format. Only JPG, JPEG, PNG, GIF, and WEBP are allowed.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T14:10:35.205000",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def upload_product_gallery_schema(func):
        """Schema for uploading product gallery images."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_upload_product_gallery",
            summary="Upload product gallery images",
            description="Upload gallery images for a specific product.",
            request={
                "multipart/form-data": serializers.PostUploadProductGalleryRequest
            },
            responses={
                200: {
                    "description": "Product gallery uploaded successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product gallery uploaded successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "ceramic-tile-floor-01",
                                },
                                "name": {
                                    "type": "string",
                                    "example": "Premium Ceramic Floor Tile",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string", "format": "uri"},
                                    "example": [
                                        "/media/uploads/products/gallery/ceramic-tile-floor-01_gallery_0.jpg",
                                        "/media/uploads/products/gallery/ceramic-tile-floor-01_gallery_1.jpg",
                                        "/media/uploads/products/gallery/ceramic-tile-floor-01_gallery_2.jpg",
                                    ],
                                },
                                "product_type": {"type": "string", "example": "lantai"},
                                "is_active": {"type": "boolean", "example": True},
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T14:25:40.800000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T14:25:40.805000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Invalid files or product not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "At least one image file is required.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T14:25:40.805000",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def delete_product_gallery_image_schema(func):
        """Schema for deleting a specific product gallery image."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_delete_product_gallery_image",
            summary="Delete product gallery image",
            description="Delete a specific image from product gallery by index.",
            responses={
                200: {
                    "description": "Gallery image deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Gallery image deleted successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "ceramic-tile-floor-01",
                                },
                                "name": {
                                    "type": "string",
                                    "example": "Premium Ceramic Floor Tile",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string", "format": "uri"},
                                    "example": [
                                        "/media/uploads/products/gallery/ceramic-tile-floor-01_gallery_0.jpg",
                                        "/media/uploads/products/gallery/ceramic-tile-floor-01_gallery_2.jpg",
                                    ],
                                },
                                "product_type": {"type": "string", "example": "lantai"},
                                "is_active": {"type": "boolean", "example": True},
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T15:05:20.300000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T15:05:20.305000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Product or gallery image not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Gallery image at index 5 does not exist for product 1.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T15:05:20.305000",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
