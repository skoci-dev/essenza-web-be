from drf_spectacular.utils import extend_schema

from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Public / Menus"]


class MenuPublicAPI:
    """API documentation for Public Menu endpoints."""

    @staticmethod
    def list_menus_schema(func):
        """Schema for listing menus."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_list_menus",
            summary="List Menus",
            description="Retrieve a list of menus.",
            auth=[],
            responses={
                200: {
                    "description": "Menus retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Menus retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "example": "Updated About",
                                    },
                                    "position": {"type": "string", "example": "header"},
                                    "items": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "label": {
                                                    "type": "string",
                                                    "example": "first menu item",
                                                },
                                                "link": {
                                                    "type": "string",
                                                    "example": "linkasas",
                                                },
                                                "order_no": {
                                                    "type": "integer",
                                                    "example": 0,
                                                },
                                                "children": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "label": {
                                                                "type": "string",
                                                                "example": "first menu item",
                                                            },
                                                            "link": {
                                                                "type": "string",
                                                                "example": "linkasas",
                                                            },
                                                            "order_no": {
                                                                "type": "integer",
                                                                "example": 0,
                                                            },
                                                            "children": {
                                                                "type": "array",
                                                                "items": {
                                                                    "type": "object",
                                                                    "properties": {
                                                                        "label": {
                                                                            "type": "string",
                                                                            "example": "first menu item",
                                                                        },
                                                                        "link": {
                                                                            "type": "string",
                                                                            "example": "linkasas",
                                                                        },
                                                                        "order_no": {
                                                                            "type": "integer",
                                                                            "example": 0,
                                                                        },
                                                                        "children": {
                                                                            "type": "array",
                                                                            "items": {
                                                                                "type": "object"
                                                                            },  # nested unlimited
                                                                        },
                                                                    },
                                                                },
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        },
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
                                    "example": "2025-12-10T02:17:08.382697",
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
