from drf_spectacular.utils import extend_schema

from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Public / Pages"]


class PagePublicAPI:
    """API documentation for Public Page endpoints."""

    @staticmethod
    def list_pages_schema(func):
        """Schema for listing pages."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_list_pages",
            summary="List Pages",
            description="Retrieve a paginated list of pages.",
            auth=[],
            parameters=DEFAULT_PAGINATION_PARAMS,
            responses={
                200: {
                    "description": "Pages retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Pages retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "slug": {"type": "string", "example": "slug"},
                                    "title": {"type": "string", "example": "title"},
                                    "meta_title": {
                                        "type": "string",
                                        "example": "meta title",
                                    },
                                    "meta_description": {
                                        "type": "string",
                                        "example": "meta description",
                                    },
                                    "meta_keywords": {
                                        "type": "string",
                                        "example": "meta keywords",
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
                                    "example": "2025-12-10T01:42:13.305040",
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

    @staticmethod
    def retrieve_page_schema(func):
        """Schema for retrieving a specific page by slug."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_retrieve_page",
            summary="Retrieve Page",
            description="Retrieve a specific page by its slug.",
            auth=[],
            responses={
                200: {
                    "description": "Page retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Page retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "slug": {"type": "string", "example": "slug"},
                                "title": {"type": "string", "example": "title"},
                                "content": {"type": "string", "example": "content"},
                                "meta_title": {
                                    "type": "string",
                                    "example": "meta title",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "meta description",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "meta keywords",
                                },
                                "template": {"type": "string", "example": "template"},
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-10T01:44:56.014635",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Page with slug not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Page with slug 'none' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-10T01:45:37.556433",
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
