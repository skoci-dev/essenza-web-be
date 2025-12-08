from drf_spectacular.utils import extend_schema

from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Public / Projects"]


class ProjectPublicAPI:
    """API documentation for Public Project endpoints."""

    @staticmethod
    def list_projects_schema(func):
        """Schema for listing projects."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_list_projects",
            summary="List Projects",
            description="Retrieve a paginated list of projects.",
            auth=[],
            parameters=DEFAULT_PAGINATION_PARAMS,
            responses={
                200: {
                    "description": "Projects retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Projects retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string", "example": "string"},
                                    "slug": {"type": "string", "example": "string"},
                                    "location": {"type": "string", "example": "string"},
                                    "description": {
                                        "type": "string",
                                        "example": "string",
                                    },
                                    "image": {
                                        "type": "string",
                                        "format": "uri",
                                        "example": "/media/uploads/project/Screenshot_2025-11-28_at_01.40.54.png",
                                    },
                                    "meta_title": {
                                        "type": "string",
                                        "example": "string",
                                    },
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
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-09T00:16:37.977065",
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
    def retrieve_project_schema(func):
        """Schema for retrieving a specific project by slug."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_retrieve_project",
            summary="Retrieve Project",
            description="Retrieve details of a specific project by its slug.",
            auth=[],
            responses={
                200: {
                    "description": "Project retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Project retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string", "example": "string"},
                                "slug": {"type": "string", "example": "string"},
                                "location": {"type": "string", "example": "string"},
                                "description": {"type": "string", "example": "string"},
                                "image": {
                                    "type": "string",
                                    "example": "/media/uploads/project/Screenshot_2025-11-28_at_01.40.54.png",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "example": [
                                        "media/uploads/projects/gallery/string_gallery_0.png",
                                        "media/uploads/projects/gallery/string_gallery_1.png",
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
                                    "example": "2025-12-09T00:18:16.079421",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Project not found.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Project with slug 'none' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-09T00:20:55.300421",
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
