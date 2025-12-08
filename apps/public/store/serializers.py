from rest_framework import serializers

from core.models import Store


class StoreCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        exclude = ["id", "created_at"]
