from rest_framework import serializers

from core.models import Menu, MenuItem


class MenuItemNestedSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ["label", "link", "children", "order_no"]

    def get_children(self, obj):
        children = obj.children.all().order_by("order_no")
        return MenuItemNestedSerializer(children, many=True).data


class MenuCollectionSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ["name", "position", "items"]

    def get_items(self, obj):
        items = obj.items.filter(parent__isnull=True).order_by("order_no")
        return MenuItemNestedSerializer(items, many=True).data
