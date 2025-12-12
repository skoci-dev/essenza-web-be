from core.dto import BaseDTO, dataclass, field


@dataclass
class FilterSettingsDTO(BaseDTO):
    """DTO for filtering settings."""

    is_active: bool | None = field(default=None)
