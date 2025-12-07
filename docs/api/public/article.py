from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Public / Articles"]


class ArticlePublicAPI:
    """API documentation for Public Article endpoints."""

    @staticmethod
    def list_articles_schema(func):
        """Schema for listing articles."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_list_articles",
            summary="List Articles",
            description="Retrieve a paginated list of articles with optional search and filtering.",
            auth=[],
            parameters=[
                *DEFAULT_PAGINATION_PARAMS,
                OpenApiParameter(
                    name="search",
                    description="Search term for filtering articles by title or content.",
                    required=False,
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                ),
            ],
            responses={
                200: {
                    "description": "Articles retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Articles retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "slug": {
                                        "type": "string",
                                        "example": "panduan-microservices-go-grpc",
                                    },
                                    "title": {
                                        "type": "string",
                                        "example": "Panduan Lengkap Membangun Microservices dengan Go dan gRPC",
                                    },
                                    "thumbnail": {
                                        "type": ["string", "null"],
                                        "example": "/media/uploads/articles/thumbnails/IOS_qwerty.png",
                                    },
                                    "snippet_content": {
                                        "type": "string",
                                        "example": "Ringkasan konten artikel...",
                                    },
                                    "author": {
                                        "type": "string",
                                        "example": "Aziz Ruri",
                                    },
                                    "tags": {
                                        "type": "string",
                                        "example": "go,microservices,grpc,backend,architecture",
                                    },
                                    "published_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-01-12T17:30:00+07:00",
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
                                    "example": "2025-12-08T00:28:09.146399",
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

    @staticmethod
    def retrieve_article_schema(func):
        """Schema for retrieving a specific article."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_retrieve_article",
            summary="Retrieve Article",
            description="Retrieve detailed information about a specific article by its slug.",
            auth=[],
            responses={
                200: {
                    "description": "Article retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Article retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "example": "Strategi Optimasi Infrastruktur Backend untuk Aplikasi dengan Traffic Tinggi",
                                },
                                "slug": {
                                    "type": "string",
                                    "example": "strategi-optimasi-infrastruktur-backend-untuk-aplikasi-dengan-traffic-tinggi",
                                },
                                "content": {"type": "string"},
                                "thumbnail": {
                                    "type": ["string", "null"],
                                    "example": "/media/uploads/articles/thumbnails/IOS_0ehTI0N.png",
                                },
                                "author": {"type": "string", "example": ""},
                                "tags": {"type": "string", "example": ""},
                                "meta_title": {"type": "string", "example": ""},
                                "meta_description": {"type": "string", "example": ""},
                                "meta_keywords": {"type": "string", "example": ""},
                                "published_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-03-18T21:10:00+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-07T22:10:04+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-08T00:30:04.721818",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Article not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Article with slug 'nott' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-08T00:30:45.256749",
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
