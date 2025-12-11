from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from utils import api_response
from services import DistributorService
from docs.api.public import DistributorPublicAPI
from services.distributor import dto

from . import serializers


class DistributorPublicViewSet(BaseViewSet):
    """Public ViewSet for managing distributor links."""

    _distributor_service = DistributorService()

    @DistributorPublicAPI.list_distributors_schema
    def list_distributors(self, request: Request) -> Response:
        """List all distributor links."""
        str_page_number = request.query_params.get("page", "1")
        str_page_size = request.query_params.get("page_size", "20")
        city = request.query_params.get("city", None)
        name = request.query_params.get("name", None)

        page = DistributorPublicViewSet._distributor_service.get_paginated_distributors(
            str_page_number=str_page_number,
            str_page_size=str_page_size,
            filters=(
                dto.FilterDistributorDTO(city=city, name=name) if city or name else None
            ),
        )

        return api_response(request).paginated(
            message="Distributor links retrieved successfully.",
            data=serializers.DistributorCollectionSerializer(page, many=True).data,
            page=page,
        )

    def get_available_cities(self, request: Request) -> Response:
        """Get a list of available cities with distributors."""
        cities = self._distributor_service.get_available_cities()

        return api_response(request).success(
            message="Available cities retrieved successfully.",
            data=serializers.IndonesianCitySerializer(cities, many=True).data,
        )
