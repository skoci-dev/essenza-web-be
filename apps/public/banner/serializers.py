from rest_framework import serializers

from core.models import Banner


class BannerCollectionSerializer(serializers.ModelSerializer):
    """Serializer for banner collection response."""

    class Meta:
        model = Banner
        exclude = ["id", "is_active", "created_at", "updated_at"]
