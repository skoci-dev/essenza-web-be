from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Public / Products"]


class ProductPublicAPI:
    """API documentation for Public Product endpoints."""

    @staticmethod
    def list_products_schema(func):
        """Schema for listing products."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_list_products",
            summary="List Products",
            description="Retrieve a paginated list of active products.",
            auth=[],
            parameters=[
                *DEFAULT_PAGINATION_PARAMS,
                OpenApiParameter(
                    name="search",
                    description="Search term for filtering products.",
                    required=False,
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                ),
            ],
            responses={
                200: {
                    "description": "Products retrieved successfully.",
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
                                    "slug": {"type": "string", "example": "stringaaa"},
                                    "name": {"type": "string", "example": "stringsasa"},
                                    "image": {
                                        "type": "string",
                                        "example": "/media/uploads/products/example.jpg",
                                    },
                                    "product_type": {
                                        "type": "string",
                                        "example": "lantai",
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
                                    "example": "2025-12-10T00:26:46.510160",
                                },
                                "pagination": {
                                    "type": "object",
                                    "properties": {
                                        "current_page": {
                                            "type": "integer",
                                            "example": 1,
                                        },
                                        "per_page": {
                                            "type": "integer",
                                            "example": 20,
                                        },
                                        "total_pages": {
                                            "type": "integer",
                                            "example": 1,
                                        },
                                        "total_items": {
                                            "type": "integer",
                                            "example": 7,
                                        },
                                        "has_next": {
                                            "type": "boolean",
                                            "example": False,
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
                }
            },
        )
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def retrieve_product_schema(func):
        """Schema for retrieving a specific product by slug."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_retrieve_product",
            summary="Retrieve Product",
            description="Retrieve details of a specific product by its slug.",
            auth=[],
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
                                "slug": {"type": "string", "example": "string-1"},
                                "name": {"type": "string", "example": "string"},
                                "description": {"type": "string", "example": "string"},
                                "image": {
                                    "type": "string",
                                    "example": "/media/uploads/products/IOS_FjSBrsy.png",
                                },
                                "product_type": {"type": "string", "example": "lantai"},
                                "brochure": {
                                    "type": "object",
                                    "properties": {
                                        "title": {
                                            "type": "string",
                                            "example": "stringa",
                                        },
                                        "file_url": {
                                            "type": "string",
                                            "example": "/media/uploads/brochure/dummies.pdf",
                                        },
                                    },
                                },
                                "variants": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "model": {
                                                "type": "string",
                                                "example": "model 1",
                                            },
                                            "size": {
                                                "type": "string",
                                                "example": "60x60",
                                            },
                                            "description": {
                                                "type": "string",
                                                "example": "string",
                                            },
                                            "image": {
                                                "type": ["string", "null"],
                                                "example": "/media/uploads/products/variants/example.jpg",
                                            },
                                            "specifications": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "label": {
                                                            "type": "string",
                                                            "example": "Color",
                                                        },
                                                        "icon": {
                                                            "type": "string",
                                                            "example": "pallete",
                                                        },
                                                        "value": {
                                                            "type": "string",
                                                            "example": "red",
                                                        },
                                                        "highlighted": {
                                                            "type": "boolean",
                                                            "example": False,
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "example": [
                                        "media/uploads/products/gallery/string-1_gallery_0.png",
                                        "media/uploads/products/gallery/string-1_gallery_1.png",
                                    ],
                                },
                                "meta_title": {"type": "string", "example": "string"},
                                "meta_description": {
                                    "type": "string",
                                    "example": "string",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "string",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-10T00:27:41.806806",
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
                            "example": "Product with slug 'none' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-10T00:28:41.397910",
                                }
                            },
                        },
                    },
                },
            },
        )
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
