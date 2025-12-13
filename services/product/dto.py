"""
Product Data Transfer Objects (DTOs)
Contains all DTOs for product-related operations
"""

from typing import List
from django.core.files.uploadedfile import InMemoryUploadedFile

from core.dto import BaseDTO, dataclass, field


@dataclass
class CreateProductDTO(BaseDTO):
    """DTO for creating a new product."""

    slug: str
    name: str
    category: str
    description: str | None = field(default=None)
    product_type: str | None = field(default=None)
    image: InMemoryUploadedFile | str | None = field(default=None)
    gallery: List[InMemoryUploadedFile] | List[str] | None = field(default=None)
    brochure_id: int | None = field(default=None)
    meta_title: str | None = field(default=None)
    meta_description: str | None = field(default=None)
    meta_keywords: str | None = field(default=None)
    is_active: bool = field(default=True)


@dataclass
class UpdateProductDTO(BaseDTO):
    """DTO for updating an existing product."""

    slug: str | None = field(default=None)
    name: str | None = field(default=None)
    category: str | None = field(default=None)
    description: str | None = field(default=None)
    product_type: str | None = field(default=None)
    image: InMemoryUploadedFile | str | None = field(default=None)
    gallery: List[InMemoryUploadedFile] | List[str] | None = field(default=None)
    brochure_id: int | None = field(default=None)
    meta_title: str | None = field(default=None)
    meta_description: str | None = field(default=None)
    meta_keywords: str | None = field(default=None)
    is_active: bool | None = field(default=None)


@dataclass
class ToggleProductStatusDTO(BaseDTO):
    """DTO for toggling product active status."""

    is_active: bool


@dataclass
class UpdateProductImageDTO(BaseDTO):
    """DTO for updating product main image."""

    image: InMemoryUploadedFile


@dataclass
class UpdateProductGalleryDTO(BaseDTO):
    """DTO for updating product gallery images."""

    gallery: List[InMemoryUploadedFile]


@dataclass
class ProductFilterDTO(BaseDTO):
    """DTO for filtering products."""

    product_type: str | None = field(default=None)
    search: str | None = field(default=None)
    is_active: bool | None = field(default=None)
    fulltext_search: str | None = field(default=None)
    sort_by: str | None = field(default=None)
    sort_order: str | None = field(default=None)


@dataclass
class CreateProductSpecificationItemDTO(BaseDTO):
    """DTO for a single product specification item."""

    slug: str
    value: str
    highlighted: bool | None = field(default=None)
    id: int | None = field(default=None)
    deleted: bool | None = field(default=None)
