from django.db import models
from core.models._base import TimeStampedModel
from core.models import Product
from core.models.specification import Specification


class ProductSpecification(TimeStampedModel):
    id = models.BigAutoField(primary_key=True, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_specifications",
    )
    specification = models.ForeignKey(
        Specification,
        on_delete=models.CASCADE,
        related_name="product_specifications",
    )
    value = models.TextField()
    highlighted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "product_specifications"

    def __str__(self) -> str:
        return f"{self.id}: {self.product} - {self.specification.label}: {self.value}"
