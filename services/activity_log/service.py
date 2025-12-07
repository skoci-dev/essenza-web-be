import logging
from typing import Optional

from django.db.models.manager import BaseManager
from core.service import BaseService
from core.models import ActivityLog

from . import dto

logger = logging.getLogger(__name__)


class ActivityLogService(BaseService):
    """Service class for activity log operations."""

    def get_activity_logs(
        self, filters: Optional[dto.FilterActivityLogsDTO]
    ) -> BaseManager[ActivityLog]:
        """Retrieve activity logs."""
        queryset = ActivityLog.objects.select_related("user")

        if filters:
            if filters.actor_type is not None:
                queryset = queryset.filter(actor_type=filters.actor_type)
            if filters.actor_identifier is not None:
                queryset = queryset.filter(
                    actor_identifier__icontains=filters.actor_identifier
                )
            if filters.actor_name is not None:
                queryset = queryset.filter(actor_name__icontains=filters.actor_name)

        return queryset.order_by("-created_at")

    def get_paginated_activity_logs(
        self,
        str_page_number: str,
        str_page_size: str,
        filters: Optional[dto.FilterActivityLogsDTO],
    ):
        """Retrieve paginated activity logs."""
        queryset = self.get_activity_logs(filters)
        return self.get_paginated_data(queryset, str_page_number, str_page_size)

    def get_specific_activity_log(self, log_id: int) -> Optional[ActivityLog]:
        """Retrieve a specific activity log by ID."""
        try:
            return ActivityLog.objects.select_related("user").get(id=log_id)
        except ActivityLog.DoesNotExist:
            logger.warning(f"ActivityLog with id {log_id} does not exist.")
            return None
