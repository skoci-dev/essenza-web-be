from django.db import models
from core.models._base import TimeStampedModel
from core.models.product_variant import ProductVariant
from core.models.specification import Specification


class ProductSpecification(TimeStampedModel):
    id = models.BigAutoField(primary_key=True, editable=False)
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="product_specifications",
    )
    specification = models.ForeignKey(
        Specification,
        on_delete=models.CASCADE,
        related_name="product_specifications",
    )
    value = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "product_specifications"

    def __str__(self) -> str:
        return f"{self.id}: {self.product_variant} - {self.specification.label}: {self.value}"
