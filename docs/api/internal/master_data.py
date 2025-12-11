from functools import wraps
from drf_spectacular.utils import extend_schema

TAGS = ["Internal / Master Data"]


class MasterDataAPI:
    """API documentation schemas for Master Data endpoints."""

    @staticmethod
    def get_all_cities_schema(func):
        """Schema for the 'Get All Cities' endpoint."""

        @extend_schema(
            tags=TAGS,
            summary="Retrieve All Indonesian Cities",
            description="Fetch a comprehensive list of all Indonesian cities available in the system.",
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
