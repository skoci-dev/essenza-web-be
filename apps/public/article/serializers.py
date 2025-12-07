from rest_framework import serializers
from core.models import Article
from utils import search_result_snippet


class ArticleCollectionSerializer(serializers.ModelSerializer):
    """Serializer for article collection response."""

    snippet_content = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "slug",
            "title",
            "thumbnail",
            "snippet_content",
            "author",
            "tags",
            "published_at",
        ]

    def get_snippet_content(self, obj: Article) -> str:
        """Return first 300 characters of content with ellipsis."""
        if search := self.context.get("search"):
            return search_result_snippet(search, obj.content or "")
        return obj.content or ""


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Serializer for article detail response."""

    class Meta:
        model = Article
        exclude = ["id", "created_at", "is_active"]
