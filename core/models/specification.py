from django.db import models
from core.models._base import TimeStampedModel


class Specification(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    slug = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255, default="")
    label = models.CharField(max_length=255)
    icon = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    order_number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: list[str] = ["label", "-created_at"]
        db_table: str = "specifications"

    def __str__(self) -> str:
        return f"{self.id}: {self.label}"
