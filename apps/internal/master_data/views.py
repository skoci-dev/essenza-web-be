from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required
from utils import api_response
from services import MasterDataService
from docs.api.internal import MasterDataAPI

from . import serializers


class MasterDataViewSet(BaseViewSet):
    """ViewSet for comprehensive master data management operations."""

    _master_data_service = MasterDataService()

    @MasterDataAPI.get_all_cities_schema
    @jwt_required
    def get_all_cities(self, request: Request) -> Response:
        """Retrieve a list of all available Indonesian cities."""
        cities = self._master_data_service.all_cities()

        return api_response(request).success(
            message="List of Indonesian cities retrieved successfully.",
            data=serializers.IndonesianCitySerializer(cities, many=True).data,
        )
