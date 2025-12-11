"""
Product Category URL Configuration
"""

from django.urls import path

from .views import ProductCategoryViewSet


urlpatterns = [
    path(
        "",
        ProductCategoryViewSet.as_view(
            {"post": "create_product_category", "get": "list_product_categories"}
        ),
    ),
    path(
        "/<slug:slug>",
        ProductCategoryViewSet.as_view(
            {
                "get": "retrieve_product_category",
                "put": "update_product_category",
                "delete": "delete_product_category",
            }
        ),
    ),
]
