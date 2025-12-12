from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

TAGS = ["Public / Settings"]


class SettingPublicAPI:
    """API documentation for Public Setting endpoints."""

    @staticmethod
    def list_settings_schema(func):
        """Schema for listing application settings."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_list_settings",
            summary="List Application Settings",
            description="Retrieve a list of all active application settings.",
            auth=[],
            responses={
                200: {
                    "description": "Settings retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Settings retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "slug": {"type": "string", "example": "stringaasa"},
                                    "label": {"type": "string", "example": "string"},
                                    "value": {"type": "string", "example": "string"},
                                    "description": {
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
                                    "example": "2025-12-12T11:28:12.401094",
                                }
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
    def retrieve_setting_schema(func):
        """Schema for retrieving a specific setting by slug."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_retrieve_setting",
            summary="Retrieve Application Setting",
            description="Retrieve a specific application setting by its slug.",
            auth=[],
            responses={
                200: {
                    "description": "Setting retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Setting retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "slug": {"type": "string", "example": "string"},
                                "label": {"type": "string", "example": "string"},
                                "value": {"type": "string", "example": "string"},
                                "description": {"type": "string", "example": "string"},
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-12T11:29:06.914365",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Setting not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Setting with slug 'none' not found.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-12T11:30:12.476783",
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
