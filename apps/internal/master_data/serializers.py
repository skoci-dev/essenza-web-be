from rest_framework import serializers

from core.enums import IndonesianCity


class IndonesianCitySerializer(serializers.Serializer):
    """Serializer for Indonesian city choices."""

    slug = serializers.CharField(source="value")
    label = serializers.CharField()
