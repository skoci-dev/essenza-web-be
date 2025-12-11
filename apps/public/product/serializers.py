from rest_framework import serializers

from core.models import Product, ProductSpecification, Brochure


class ProductCollectionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", allow_null=True)

    class Meta:
        model = Product
        fields = ["slug", "name", "image", "product_type", "category"]


class BrochureNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brochure
        fields = ["title", "file_url"]


class SpecificationNestedSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(source="specification.slug")
    label = serializers.CharField(source="specification.label")
    icon = serializers.CharField(source="specification.icon")
    order_number = serializers.IntegerField(source="specification.order_number")

    class Meta:
        model = ProductSpecification
        fields = ["slug", "label", "icon", "value", "highlighted", "order_number"]


class ProductDetailSerializer(serializers.ModelSerializer):
    brochure = BrochureNestedSerializer()
    category = serializers.CharField(source="category.name", allow_null=True)
    specifications = SpecificationNestedSerializer(
        source="product_specifications", many=True
    )

    class Meta:
        model = Product
        fields = [
            "slug",
            "name",
            "category",
            "description",
            "image",
            "product_type",
            "brochure",
            "gallery",
            "meta_title",
            "meta_description",
            "meta_keywords",
            "specifications",
        ]
