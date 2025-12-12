from django.db import models
from core.models._base import TimeStampedModel, FileUploadModel, upload_to
from core.enums import ProductType
from core.models.brochure import Brochure
from core.models.product_category import ProductCategory


class Product(TimeStampedModel, FileUploadModel):
    id = models.BigAutoField(primary_key=True, editable=False)
    slug: models.CharField = models.CharField(max_length=255, unique=True)
    category: models.ForeignKey = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name: models.CharField = models.CharField(max_length=255)
    lang: models.CharField = models.CharField(max_length=10, default="en")
    description: models.TextField = models.TextField(blank=True)
    product_type: models.CharField = models.CharField(
        max_length=20, choices=ProductType.choices, blank=True
    )
    image: models.ImageField = models.ImageField(
        upload_to=upload_to("products"), blank=True
    )
    gallery: models.JSONField = models.JSONField(blank=True)
    brochure: models.ForeignKey = models.ForeignKey(
        Brochure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    meta_title: models.CharField = models.CharField(max_length=255, blank=True)
    meta_description: models.TextField = models.TextField(blank=True)
    meta_keywords: models.TextField = models.TextField(blank=True)
    is_active: models.BooleanField = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "products"

    def __str__(self) -> str:
        return f"{self.id}: {self.name}"

    def get_product_type_enum(self) -> ProductType | None:
        """Get the ProductType enum instance for the product_type field."""
        try:
            return ProductType(self.product_type)
        except ValueError:
            return None
