from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Public / Distributors"]


class DistributorPublicAPI:
    """API documentation for Public Distributor endpoints."""

    @staticmethod
    def list_distributors_schema(func):
        """Schema for listing distributor links."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_list_distributors",
            summary="List Distributor Links",
            description="Retrieve a paginated list of distributor links.",
            auth=[],
            parameters=[
                *DEFAULT_PAGINATION_PARAMS,
                OpenApiParameter(
                    name="name",
                    description="Search distributors by name (case-insensitive, partial match).",
                    required=False,
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                ),
                OpenApiParameter(
                    name="city",
                    description="Filter distributors by city slug.",
                    required=False,
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                ),
            ],
            responses={
                200: {
                    "description": "Distributor links retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Distributor links retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "example": "UD Maju Bersama",
                                    },
                                    "address": {
                                        "type": "string",
                                        "example": "Jl. Diponegoro No. 45, Surabaya",
                                    },
                                    "phone": {
                                        "type": "string",
                                        "example": "6282222223333",
                                    },
                                    "email": {
                                        "type": "string",
                                        "example": "sales@majubersama.id",
                                    },
                                    "website": {
                                        "type": "string",
                                        "example": "https://majubersama.id",
                                    },
                                    "latitude": {
                                        "type": "string",
                                        "example": "-7.257472",
                                    },
                                    "longitude": {
                                        "type": "string",
                                        "example": "112.752090",
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
                                            "example": 3,
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
    def get_available_cities_schema(func):
        """Schema for getting available cities with distributors."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_distributors_get_available_cities",
            summary="Get Available Cities with Distributors",
            description="Retrieve a list of cities that have distributors.",
            auth=[],
        )
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
