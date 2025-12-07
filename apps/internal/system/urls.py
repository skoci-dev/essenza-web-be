from django.urls import path

from .views import SystemViewSet

urlpatterns = [
    path(
        "/status",
        SystemViewSet.as_view({"get": "get_system_status"}),
        name="system_status",
    ),
    path(
        "/metrics",
        SystemViewSet.as_view({"get": "get_system_metrics"}),
        name="system_metrics",
    ),
    path(
        "/activity-logs",
        SystemViewSet.as_view({"get": "get_activity_logs"}),
        name="activity_logs",
    ),
    path(
        "/activity-logs/<int:log_id>",
        SystemViewSet.as_view({"get": "get_specific_activity_log"}),
        name="specific_activity_log",
    ),
]
