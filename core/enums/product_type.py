from django.db import models


class ProductType(models.TextChoices):
    LANTAI = 'lantai', 'Lantai'
    DINDING = 'dinding', 'Dinding'
    DINDING_LANTAI = 'dinding-lantai', 'Dinding & Lantai'
