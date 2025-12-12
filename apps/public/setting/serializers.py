from rest_framework import serializers

from core.models import Setting


class SettingCollectionSerializer(serializers.ModelSerializer):
    """Serializer for setting collection response."""

    class Meta:
        model = Setting
        fields = ["slug", "label", "value", "description"]