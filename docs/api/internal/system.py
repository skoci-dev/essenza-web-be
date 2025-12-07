"""
API Documentation for System endpoints
"""

from functools import wraps
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Internal / System"]


class SystemAPI:
    """API documentation for System endpoints."""

    @staticmethod
    def get_system_status_schema(func):
        """Schema for retrieving system status."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_get_system_status",
            summary="Get System Status",
            description="Retrieve system status information including uptime, version, and platform details.",
            responses={
                200: {
                    "description": "System status retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "System status retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "status": {
                                    "type": "string",
                                    "example": "operational",
                                },
                                "uptime": {
                                    "type": "string",
                                    "example": "5d 12h 30m 15s",
                                },
                                "uptime_seconds": {
                                    "type": "integer",
                                    "example": 475815,
                                },
                                "boot_time": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-01T10:00:00",
                                },
                                "version": {"type": "string", "example": "1.0.0"},
                                "django_version": {
                                    "type": "string",
                                    "example": "4.1.13",
                                },
                                "python_version": {
                                    "type": "string",
                                    "example": "3.11.5",
                                },
                                "platform": {"type": "string", "example": "Linux"},
                                "platform_release": {
                                    "type": "string",
                                    "example": "5.15.0",
                                },
                                "hostname": {
                                    "type": "string",
                                    "example": "essenza-server",
                                },
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-07T10:30:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                }
                            },
                        },
                    },
                }
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def get_system_metrics_schema(func):
        """Schema for retrieving system metrics."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_get_system_metrics",
            summary="Get System Metrics",
            description="Retrieve detailed system metrics including CPU, memory, disk, and network usage. Metrics are cached for 30 seconds by default. Use ?refresh=true to bypass cache.",
            parameters=[
                OpenApiParameter(
                    name="refresh",
                    type=OpenApiTypes.BOOL,
                    location=OpenApiParameter.QUERY,
                    description="Force refresh metrics (bypass cache)",
                    required=False,
                    default=False,
                ),
            ],
            responses={
                200: {
                    "description": "System metrics retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "System metrics retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "cpu": {
                                    "type": "object",
                                    "properties": {
                                        "usage_percent": {
                                            "type": "number",
                                            "example": 45.5,
                                        },
                                        "count": {"type": "integer", "example": 4},
                                        "frequency_mhz": {
                                            "type": "number",
                                            "nullable": True,
                                            "example": 2400.0,
                                        },
                                    },
                                },
                                "memory": {
                                    "type": "object",
                                    "properties": {
                                        "total": {
                                            "type": "string",
                                            "example": "16.00 GB",
                                        },
                                        "available": {
                                            "type": "string",
                                            "example": "8.50 GB",
                                        },
                                        "used": {
                                            "type": "string",
                                            "example": "7.50 GB",
                                        },
                                        "usage_percent": {
                                            "type": "number",
                                            "example": 46.88,
                                        },
                                        "total_bytes": {
                                            "type": "integer",
                                            "example": 17179869184,
                                        },
                                        "available_bytes": {
                                            "type": "integer",
                                            "example": 9126805504,
                                        },
                                        "used_bytes": {
                                            "type": "integer",
                                            "example": 8053063680,
                                        },
                                    },
                                },
                                "swap": {
                                    "type": "object",
                                    "properties": {
                                        "total": {
                                            "type": "string",
                                            "example": "4.00 GB",
                                        },
                                        "used": {
                                            "type": "string",
                                            "example": "1.20 GB",
                                        },
                                        "free": {
                                            "type": "string",
                                            "example": "2.80 GB",
                                        },
                                        "usage_percent": {
                                            "type": "number",
                                            "example": 30.0,
                                        },
                                    },
                                },
                                "disk": {
                                    "type": "object",
                                    "properties": {
                                        "total": {
                                            "type": "string",
                                            "example": "500.00 GB",
                                        },
                                        "used": {
                                            "type": "string",
                                            "example": "180.00 GB",
                                        },
                                        "free": {
                                            "type": "string",
                                            "example": "320.00 GB",
                                        },
                                        "usage_percent": {
                                            "type": "number",
                                            "example": 36.0,
                                        },
                                        "total_bytes": {
                                            "type": "integer",
                                            "example": 536870912000,
                                        },
                                        "free_bytes": {
                                            "type": "integer",
                                            "example": 343597383680,
                                        },
                                    },
                                },
                                "network": {
                                    "type": "object",
                                    "nullable": True,
                                    "properties": {
                                        "bytes_sent": {
                                            "type": "string",
                                            "example": "1.50 GB",
                                        },
                                        "bytes_received": {
                                            "type": "string",
                                            "example": "3.20 GB",
                                        },
                                        "packets_sent": {
                                            "type": "integer",
                                            "example": 1234567,
                                        },
                                        "packets_received": {
                                            "type": "integer",
                                            "example": 2345678,
                                        },
                                    },
                                },
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-07T10:30:00",
                                },
                                "cached": {
                                    "type": "boolean",
                                    "example": False,
                                    "description": "Indicates if the data is from cache",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                }
                            },
                        },
                    },
                }
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def get_activity_logs_schema(func):
        """Schema for retrieving activity logs."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_get_activity_logs",
            summary="Get Activity Logs",
            description="Retrieve activity logs with optional filtering and pagination support.",
            parameters=[
                *DEFAULT_PAGINATION_PARAMS,
                OpenApiParameter(
                    name="actor_type",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Filter by actor type (user or guest)",
                    required=False,
                    enum=["user", "guest"],
                ),
                OpenApiParameter(
                    name="actor_identifier",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Filter by actor identifier (email, phone, session_id, IP)",
                    required=False,
                ),
                OpenApiParameter(
                    name="actor_name",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Filter by actor name",
                    required=False,
                ),
            ],
            responses={
                200: {
                    "description": "Activity logs retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Activity logs retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "user": {
                                        "type": "object",
                                        "nullable": True,
                                        "properties": {
                                            "id": {"type": "integer", "example": 1},
                                            "email": {
                                                "type": "string",
                                                "example": "admin@example.com",
                                            },
                                            "first_name": {
                                                "type": "string",
                                                "example": "John",
                                            },
                                            "last_name": {
                                                "type": "string",
                                                "example": "Doe",
                                            },
                                        },
                                    },
                                    "actor_type": {
                                        "type": "string",
                                        "example": "user",
                                    },
                                    "actor_type_display": {
                                        "type": "string",
                                        "example": "User",
                                    },
                                    "actor_identifier": {
                                        "type": "string",
                                        "example": "admin@example.com",
                                    },
                                    "actor_name": {
                                        "type": "string",
                                        "example": "John Doe",
                                    },
                                    "action": {
                                        "type": "string",
                                        "example": "create",
                                    },
                                    "action_display": {
                                        "type": "string",
                                        "example": "Create",
                                    },
                                    "entity": {
                                        "type": "string",
                                        "example": "product",
                                    },
                                    "entity_id": {
                                        "type": "integer",
                                        "nullable": True,
                                        "example": 123,
                                    },
                                    "entity_name": {
                                        "type": "string",
                                        "example": "Product Name",
                                    },
                                    "description": {
                                        "type": "string",
                                        "example": "Created new product",
                                    },
                                    "ip_address": {
                                        "type": "string",
                                        "nullable": True,
                                        "example": "192.168.1.1",
                                    },
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-12-07T10:30:00+07:00",
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
                                },
                                "pagination": {
                                    "type": "object",
                                    "properties": {
                                        "current_page": {"type": "integer"},
                                        "per_page": {"type": "integer"},
                                        "total_pages": {"type": "integer"},
                                        "total_items": {"type": "integer"},
                                        "has_next": {"type": "boolean"},
                                        "has_previous": {"type": "boolean"},
                                    },
                                },
                            },
                        },
                    },
                }
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def get_specific_activity_log_schema(func):
        """Schema for retrieving a specific activity log."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_get_specific_activity_log",
            summary="Get Specific Activity Log",
            description="Retrieve a specific activity log by its ID.",
            responses={
                200: {
                    "description": "Activity log retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Activity log retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 26},
                                "user": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer", "example": 1},
                                        "username": {
                                            "type": "string",
                                            "example": "ruriazz",
                                        },
                                        "name": {
                                            "type": "string",
                                            "example": "ruri aziz",
                                        },
                                        "email": {
                                            "type": "string",
                                            "example": "me@ruriazz.com",
                                        },
                                    },
                                },
                                "actor_type": {"type": "string", "example": "user"},
                                "action": {"type": "string", "example": "create"},
                                "actor_identifier": {
                                    "type": "string",
                                    "example": "me@ruriazz.com",
                                },
                                "actor_name": {
                                    "type": "string",
                                    "example": "ruri aziz",
                                },
                                "actor_metadata": {"type": "object", "example": "null"},
                                "entity": {
                                    "type": "string",
                                    "example": "productvariant",
                                },
                                "entity_id": {"type": "integer", "example": 4},
                                "entity_name": {
                                    "type": "string",
                                    "example": "4: model 3 - string",
                                },
                                "old_values": {"type": "object", "example": "null"},
                                "new_values": {
                                    "type": "object",
                                    "properties": {
                                        "product": {"type": "integer", "example": 2},
                                        "sku": {"type": "string", "example": ""},
                                        "model": {
                                            "type": "string",
                                            "example": "model 3",
                                        },
                                        "size": {"type": "string", "example": ""},
                                        "description": {
                                            "type": "string",
                                            "example": "",
                                        },
                                        "image": {
                                            "type": "string",
                                            "example": "/media/uploads/products/variants/trotoar-scbd_udMzant_gO8IsBW.jpg",
                                        },
                                        "is_active": {
                                            "type": "boolean",
                                            "example": True,
                                        },
                                    },
                                },
                                "changed_fields": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "description": {
                                    "type": "string",
                                    "example": "Product variant created with specifications",
                                },
                                "ip_address": {
                                    "type": "string",
                                    "example": "127.0.0.1",
                                },
                                "user_agent": {
                                    "type": "string",
                                    "example": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                                },
                                "extra_data": {"type": "object", "example": {}},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T21:33:20.641990+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-07T21:35:46.731684",
                                },
                            },
                        },
                    },
                },
                404: {
                    "description": "Activity log not found.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "Activity log with ID 2611 not found.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-07T21:37:01.212805",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
