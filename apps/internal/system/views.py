"""
System ViewSet for Internal Application
Handles system-related API endpoints including activity logs.
"""

import logging
from rest_framework.request import Request
from rest_framework.response import Response

from core.decorators.validation import validate_query_params
from core.views import BaseViewSet
from core.decorators import jwt_required
from utils import api_response
from services import ActivityLogService, SystemService
from services.activity_log import dto
from docs.api.internal import SystemAPI

from . import serializers

logger = logging.getLogger(__name__)


class SystemViewSet(BaseViewSet):
    """ViewSet for system-related operations."""

    _activity_log_service = ActivityLogService()
    _system_service = SystemService()

    @SystemAPI.get_system_status_schema
    @jwt_required
    def get_system_status(self, request: Request) -> Response:
        """Retrieve system status information."""
        try:
            logger.debug("Fetching system status.")
            status_info = self._system_service.get_system_status()

            return api_response(request).success(
                message="System status retrieved successfully.", data=status_info
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in get_system_status: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while retrieving system status."
            )

    @SystemAPI.get_system_metrics_schema
    @jwt_required
    def get_system_metrics(self, request: Request) -> Response:
        """Retrieve system metrics."""
        try:
            logger.debug("Fetching system metrics.")

            # Check if refresh parameter is provided to bypass cache
            refresh = request.GET.get("refresh", "false").lower() in (
                "true",
                "1",
                "yes",
            )
            use_cache = not refresh

            metrics = self._system_service.get_system_metrics(use_cache=use_cache)

            return api_response(request).success(
                message="System metrics retrieved successfully.", data=metrics
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in get_system_metrics: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while retrieving system metrics."
            )

    @SystemAPI.get_activity_logs_schema
    @jwt_required
    @validate_query_params(serializers.GetActivityLogsQuerySerializer)
    def get_activity_logs(self, request: Request, validated_data) -> Response:
        """Retrieve activity logs with optional filtering and pagination."""
        try:
            page_number = validated_data.get("page", "1")
            page_size = validated_data.get("page_size", "20")

            # Build filters from query parameters
            filters = None
            actor_type = validated_data.get("actor_type")
            actor_identifier = validated_data.get("actor_identifier")
            actor_name = validated_data.get("actor_name")

            if actor_type or actor_identifier or actor_name:
                filters = dto.FilterActivityLogsDTO(
                    actor_type=actor_type or None,
                    actor_identifier=actor_identifier or None,
                    actor_name=actor_name or None,
                )

            logger.info(f"Retrieving activity logs with filters: {filters}")

            page = self._activity_log_service.get_paginated_activity_logs(
                str_page_number=page_number,
                str_page_size=page_size,
                filters=filters,
            )

            return api_response(request).paginated(
                message="Activity logs retrieved successfully.",
                data=serializers.MinimalActivityLogModelSerializer(
                    page, many=True
                ).data,
                page=page,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in get_activity_logs: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while retrieving activity logs."
            )

    @SystemAPI.get_specific_activity_log_schema
    @jwt_required
    def get_specific_activity_log(self, request: Request, log_id: int) -> Response:
        """Retrieve a specific activity log by ID."""
        if activity_log := self._activity_log_service.get_specific_activity_log(
            log_id=log_id
        ):
            return api_response(request).success(
                message="Activity log retrieved successfully.",
                data=serializers.ActivityLogModelSerializer(activity_log).data,
            )
        return api_response(request).not_found(
            message=f"Activity log with ID {log_id} not found."
        )
