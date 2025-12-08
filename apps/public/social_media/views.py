from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from utils import api_response
from services import SocialMediaService
from docs.api.public import SocialMediaPublicAPI

from . import serializers


class SocialMediaPublicViewSet(BaseViewSet):
    """Public ViewSet for managing social media links."""

    _social_media_service = SocialMediaService()

    @SocialMediaPublicAPI.list_social_media_schema
    def list_social_media(self, request: Request) -> Response:
        """List all social media links."""
        str_page_number = request.query_params.get("page", "1")
        str_page_size = request.query_params.get("page_size", "20")

        page = self._social_media_service.get_social_media_list(
            str_page_number=str_page_number,
            str_page_size=str_page_size,
        )
        return api_response(request).paginated(
            message="Social media links retrieved successfully.",
            data=serializers.SocialMediaCollectionSerializer(
                page.object_list, many=True
            ).data,
            page=page,
        )
