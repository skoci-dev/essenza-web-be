from core.service import BaseService
from core.enums import IndonesianCity


class MasterDataService(BaseService):
    """Service class for managing master data operations."""

    def all_cities(self) -> list[IndonesianCity]:
        """Retrieve a list of all available cities."""
        return list(IndonesianCity)
