"""
Serializers for System API endpoints
"""

from rest_framework import serializers

from core.models import ActivityLog, User
from core.enums import ActorType, ActionType


class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer for User model in activity logs."""

    class Meta:
        model = User
        fields = ["id", "username", "name", "email"]


class ActivityLogModelSerializer(serializers.ModelSerializer):
    """Serializer for ActivityLog model."""

    user = UserMinimalSerializer(read_only=True)
    actor_type = serializers.ChoiceField(choices=ActorType.choices)
    action = serializers.ChoiceField(choices=ActionType.choices)

    class Meta:
        model = ActivityLog
        read_only_fields = ["id", "created_at"]
        exclude = ["computed_entity"]


class MinimalActivityLogModelSerializer(serializers.ModelSerializer):
    """Serializer for ActivityLog model."""

    user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "user",
            "actor_type",
            "actor_identifier",
            "actor_name",
            "action",
            "description",
            "ip_address",
            "user_agent",
        ]
        read_only_fields = ["id", "created_at"]


class GetActivityLogsQuerySerializer(serializers.Serializer):
    """Serializer for validating query parameters for activity logs."""

    page = serializers.IntegerField(default=1, min_value=1, required=False)
    page_size = serializers.IntegerField(
        default=20, min_value=1, max_value=100, required=False
    )
    actor_type = serializers.ChoiceField(
        choices=ActorType.choices, required=False, allow_null=True
    )
    actor_identifier = serializers.CharField(
        max_length=255, required=False, allow_null=True, allow_blank=True
    )
    actor_name = serializers.CharField(
        max_length=255, required=False, allow_null=True, allow_blank=True
    )
