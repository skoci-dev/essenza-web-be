from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from utils import api_response
from services import DistributorService
from docs.api.public import DistributorPublicAPI

from . import serializers


class DistributorPublicViewSet(BaseViewSet):
    """Public ViewSet for managing distributor links."""

    _distributor_service = DistributorService()

    @DistributorPublicAPI.list_distributors_schema
    def list_distributors(self, request: Request) -> Response:
        """List all distributor links."""
        str_page_number = request.query_params.get("page", "1")
        str_page_size = request.query_params.get("page_size", "20")

        page = DistributorPublicViewSet._distributor_service.get_paginated_distributors(
            str_page_number=str_page_number,
            str_page_size=str_page_size,
        )

        return api_response(request).paginated(
            message="Distributor links retrieved successfully.",
            data=serializers.DistributorCollectionSerializer(page, many=True).data,
            page=page,
        )
