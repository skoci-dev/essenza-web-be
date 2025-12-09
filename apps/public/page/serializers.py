from rest_framework import serializers

from core.models import Page


class PageCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = [
            "slug",
            "title",
            "meta_title",
            "meta_description",
            "meta_keywords",
        ]


class PageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        exclude = ["id", "is_active", "created_at", "updated_at"]