from rest_framework import serializers

from core.models import Distributor


class DistributorCollectionSerializer(serializers.ModelSerializer):
    """Serializer for distributor collection response."""

    class Meta:
        model = Distributor
        exclude = ["id", "created_at"]


class IndonesianCitySerializer(serializers.Serializer):
    """Serializer for Indonesian city choices."""

    slug = serializers.CharField(source="value")
    label = serializers.CharField()
