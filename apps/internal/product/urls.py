"""
Product API URL Configuration
Maps URL patterns to ProductViewSet actions
"""

from django.urls import path

from .views import ProductViewSet


urlpatterns = [
    path(
        "",
        ProductViewSet.as_view({"post": "create_product", "get": "get_products"}),
        name="products",
    ),
    path(
        "/<int:pk>",
        ProductViewSet.as_view(
            {
                "get": "get_specific_product",
                "put": "update_specific_product",
                "delete": "delete_specific_product",
            }
        ),
        name="specific_product",
    ),
    path(
        "/<int:pk>/toggle",
        ProductViewSet.as_view({"patch": "toggle_product_status"}),
        name="toggle_product_status",
    ),
    path(
        "/slug/<str:slug>",
        ProductViewSet.as_view({"get": "get_product_by_slug"}),
        name="product_by_slug",
    ),
    path(
        "/<int:pk>/image",
        ProductViewSet.as_view({"post": "upload_product_image"}),
        name="upload_product_image",
    ),
    path(
        "/<int:pk>/gallery",
        ProductViewSet.as_view({"post": "upload_product_gallery"}),
        name="upload_product_gallery",
    ),
    path(
        "/<int:pk>/gallery/<int:index>",
        ProductViewSet.as_view({"delete": "delete_product_gallery_image"}),
        name="delete_product_gallery_image",
    ),
]
