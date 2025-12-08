from drf_spectacular.utils import extend_schema

from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Public / Stores"]


class StorePublicAPI:
    """API documentation for Public Store endpoints."""

    @staticmethod
    def list_stores_schema(func):
        """Schema for listing store locations."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_list_stores",
            summary="List Store Locations",
            description="Retrieve a paginated list of store locations.",
            auth=[],
            parameters=DEFAULT_PAGINATION_PARAMS,
            responses={
                200: {
                    "description": "Store locations retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Store locations retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "example": "Global Store Surabaya",
                                    },
                                    "address": {
                                        "type": "string",
                                        "example": "Jl. Raya Darmo No. 88, Surabaya",
                                    },
                                    "phone": {
                                        "type": "string",
                                        "example": "6281345678901",
                                    },
                                    "email": {
                                        "type": "string",
                                        "example": "surabaya@globalstore.com",
                                    },
                                    "latitude": {
                                        "type": "string",
                                        "example": "-7.275612",
                                    },
                                    "longitude": {
                                        "type": "string",
                                        "example": "112.642643",
                                    },
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
                                            "example": 2,
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
