from django.urls import path


from .views import ProductPublicViewSet


urlpatterns = [
    path("", ProductPublicViewSet.as_view({"get": "list_products"})),
    path("/<slug:slug>", ProductPublicViewSet.as_view({"get": "retrieve_product"})),
]
