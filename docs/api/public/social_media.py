from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Public / Social Media"]


class SocialMediaPublicAPI:
    """API documentation for Public Social Media endpoints."""

    @staticmethod
    def list_social_media_schema(func):
        """Schema for listing social media links."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_list_social_media",
            summary="List Social Media Links",
            description="Retrieve a paginated list of social media links.",
            auth=[],
            parameters=DEFAULT_PAGINATION_PARAMS,
            responses={
                200: {
                    "description": "Social media links retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Social media links retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "platform": {
                                        "type": "string",
                                        "example": "Instagram",
                                    },
                                    "icon": {
                                        "type": "string",
                                        "nullable": True,
                                        "example": "string",
                                    },
                                    "url": {
                                        "type": "string",
                                        "example": "https://instagram.com",
                                    },
                                    "order_no": {"type": "integer", "example": 1},
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {"type": "string", "format": "date-time"},
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
                                            "example": 1,
                                        },
                                        "total_items": {
                                            "type": "integer",
                                            "example": 1,
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
