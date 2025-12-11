from django.db import models
from core.models._base import TimeStampedModel


class ProductCategory(TimeStampedModel):
    id = models.SmallAutoField(primary_key=True, editable=False)
    slug: models.CharField = models.CharField(max_length=255, unique=True)
    name: models.CharField = models.CharField(max_length=255)
    description: models.TextField = models.TextField(blank=True)
    is_active: models.BooleanField = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: list[str] = ["name", "-created_at"]
        db_table: str = "product_categories"

    def __str__(self) -> str:
        return f"{self.id}: {self.name}"
