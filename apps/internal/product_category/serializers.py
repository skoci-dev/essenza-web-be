from rest_framework import serializers

from core.models import ProductCategory


class ProductCategoryModelSerializer(serializers.ModelSerializer):
    """Serializer for ProductCategory model."""

    class Meta:
        model = ProductCategory
        fields = "__all__"


class PostCreateProductCategoryRequest(serializers.Serializer):
    """Serializer for creating a new product category."""

    name = serializers.CharField(
        max_length=255,
        help_text="Name of the product category",
    )
    slug = serializers.CharField(
        max_length=255,
        help_text="Slug for the product category",
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Description of the product category (optional)",
    )
    is_active = serializers.BooleanField(
        help_text="Whether the product category is active",
    )


class PutUpdateProductCategoryRequest(serializers.Serializer):
    """Serializer for updating an existing product category."""

    name = serializers.CharField(
        max_length=255,
        required=False,
        help_text="Name of the product category",
    )
    slug = serializers.CharField(
        max_length=255,
        required=False,
        help_text="Slug for the product category",
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Description of the product category (optional)",
    )
    is_active = serializers.BooleanField(
        required=False,
        help_text="Whether the product category is active",
    )
