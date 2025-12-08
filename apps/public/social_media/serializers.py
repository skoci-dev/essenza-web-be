from rest_framework import serializers

from core.models import SocialMedia


class SocialMediaCollectionSerializer(serializers.ModelSerializer):
    """Serializer for social media collection response."""

    class Meta:
        model = SocialMedia
        exclude = ["id", "created_at"]
