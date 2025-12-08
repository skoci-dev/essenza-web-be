from drf_spectacular.utils import extend_schema

from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Public / Banners"]


class BannerPublicAPI:
    """API documentation for Public Banner endpoints."""

    @staticmethod
    def list_banner_schema(func):
        """Schema for listing banner links."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_list_banners",
            summary="List Banner Links",
            description="Retrieve a paginated list of banner links.",
            auth=[],
            parameters=DEFAULT_PAGINATION_PARAMS,
            responses={
                200: {
                    "description": "Banner links retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Banner links retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string", "example": "string"},
                                    "subtitle": {"type": "string", "example": "string"},
                                    "image": {
                                        "type": "string",
                                        "example": "/media/uploads/banner/IOS.png",
                                    },
                                    "link_url": {"type": "string", "example": "string"},
                                    "order_no": {"type": "integer", "example": 0},
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
                                            "example": 6,
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
