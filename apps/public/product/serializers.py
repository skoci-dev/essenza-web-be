from rest_framework import serializers

from core.models import Product, ProductVariant, ProductSpecification, Brochure


class ProductCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "slug",
            "name",
            "image",
            "product_type",
        ]


class ProductVariantNestedSerializer(serializers.ModelSerializer):
    class ProductSpecificationNestedSerializer(serializers.ModelSerializer):
        label = serializers.CharField(source="specification.label")
        icon = serializers.CharField(source="specification.icon")

        class Meta:
            model = ProductSpecification
            fields = ["label", "icon", "value", "highlighted"]

    specifications = ProductSpecificationNestedSerializer(
        source="product_specifications", many=True
    )

    class Meta:
        model = ProductVariant
        fields = [
            "model",
            "size",
            "description",
            "image",
            "specifications",
        ]


class BrochureNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brochure
        fields = ["title", "file_url"]


class ProductDetailSerializer(serializers.ModelSerializer):
    variants = ProductVariantNestedSerializer(many=True)
    brochure = BrochureNestedSerializer()

    class Meta:
        model = Product
        fields = [
            "slug",
            "name",
            "description",
            "image",
            "product_type",
            "brochure",
            "variants",
            "gallery",
            "meta_title",
            "meta_description",
            "meta_keywords",
        ]
