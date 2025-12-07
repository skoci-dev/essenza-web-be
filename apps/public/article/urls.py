from django.urls import path

from .views import ArticlePublicViewSet


urlpatterns = [
    path("", ArticlePublicViewSet.as_view({"get": "list_articles"})),
    path(
        "<slug:article_slug>", ArticlePublicViewSet.as_view({"get": "retrieve_article"})
    ),
]
