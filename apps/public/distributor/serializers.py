from rest_framework import serializers

from core.models import Distributor


class DistributorCollectionSerializer(serializers.ModelSerializer):
    """Serializer for distributor collection response."""

    class Meta:
        model = Distributor
        exclude = ["id", "created_at"]