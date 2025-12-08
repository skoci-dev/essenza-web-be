from rest_framework import serializers

from core.models import Project


class ProjectCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ["id", "gallery", "is_active", "created_at"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ["id", "is_active", "created_at"]
