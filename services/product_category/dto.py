from core.dto import BaseDTO, dataclass, field


@dataclass
class CreateProductCategoryDTO(BaseDTO):
    """DTO for creating a new product category."""

    name: str
    slug: str
    description: str | None = field(default=None)
    is_active: bool = field(default=True)


@dataclass
class FilterProductCategoryDTO(BaseDTO):
    """DTO for filtering product categories."""

    is_active: bool | None = field(default=None)
