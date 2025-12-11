from copy import deepcopy
import logging
from typing import Tuple, Optional

from django.db.models import QuerySet
from django.db import transaction

from core.enums import ActionType
from core.service import BaseService, required_context, ServiceException
from core.models import ProductCategory

from . import dto

logger = logging.getLogger(__name__)


class ProductCategoryService(BaseService):
    """Service class for managing product categories."""

    @required_context
    def create_product_category(
        self, data: dto.CreateProductCategoryDTO
    ) -> Tuple[ProductCategory, Optional[Exception]]:
        """Create a new product category with transaction safety.

        Args:
            data: Product category creation data transfer object

        Returns:
            Tuple containing created ProductCategory instance and optional Exception
        """
        try:
            if ProductCategory.objects.filter(slug=data.slug).exists():
                raise ServiceException(
                    f"Product category with slug '{data.slug}' already exists."
                )

            with transaction.atomic():
                return self._create_product_category_with_data(data)
        except Exception as e:
            logger.error(f"Error creating product category: {e}", exc_info=True)
            return ProductCategory(), e

    @required_context
    def _create_product_category_with_data(
        self, data: dto.CreateProductCategoryDTO
    ) -> Tuple[ProductCategory, None]:
        """Create product category with processed data.

        Args:
            data: Product category creation data transfer object

        Returns:
            Tuple containing created ProductCategory instance and None
        """
        # Prepare creation data
        create_data = data.to_dict()

        # Create product category
        product_category = ProductCategory.objects.create(**create_data)
        self.log_entity_change(
            self.ctx,
            product_category,
            action=ActionType.CREATE,
            description=f"Product category '{product_category.name}' created.",
        )
        return product_category, None

    def get_product_categories(
        self, filters: Optional[dto.FilterProductCategoryDTO] = None
    ) -> QuerySet[ProductCategory]:
        """Retrieve product categories based on filters.

        Args:
            filters: Dictionary of filters to apply

        Returns:
            QuerySet of ProductCategory instances
        """
        queryset = ProductCategory.objects.all()
        if filters and filters.is_active is not None:
            queryset = queryset.filter(is_active=filters.is_active)
        return queryset

    def get_product_category_by_slug(
        self, slug: str
    ) -> Tuple[ProductCategory, Optional[Exception]]:
        """Retrieve a specific product category by its slug.

        Args:
            slug: Slug of the product category

        Returns:
            Tuple containing ProductCategory instance and optional Exception
        """
        try:
            product_category = ProductCategory.objects.get(slug=slug)
            return product_category, None
        except ProductCategory.DoesNotExist:
            return ProductCategory(), ServiceException(
                f"Product category with slug '{slug}' does not exist."
            )
        except Exception as e:
            return ProductCategory(), e

    @required_context
    def update_product_category(
        self, slug: str, data: dto.CreateProductCategoryDTO
    ) -> Tuple[ProductCategory, Optional[Exception]]:
        """Update a specific product category by its slug.

        Args:
            slug: Slug of the product category
            data: Product category update data transfer object

        Returns:
            Tuple containing updated ProductCategory instance and optional Exception
        """
        try:
            product_category = ProductCategory.objects.get(slug=slug)
            old_instance = deepcopy(product_category)

            if (
                data.slug is not None
                and data.slug != slug
                and ProductCategory.objects.filter(slug=data.slug).exists()
            ):
                raise ServiceException(
                    f"Product category with slug '{data.slug}' already exists."
                )
            for key, value in data.to_dict().items():
                setattr(product_category, key, value)
            product_category.save()
            self.log_entity_change(
                self.ctx,
                instance=product_category,
                old_instance=old_instance,
                action=ActionType.UPDATE,
                description=f"Product category '{product_category.name}' updated.",
            )
            return product_category, None
        except ProductCategory.DoesNotExist:
            return ProductCategory(), ServiceException(
                f"Product category with slug '{slug}' does not exist."
            )
        except Exception as e:
            return ProductCategory(), e

    @required_context
    def delete_product_category(self, slug: str) -> Optional[Exception]:
        """Delete a specific product category by its slug.

        Args:
            slug: Slug of the product category

        Returns:
            Optional Exception if an error occurs
        """
        try:
            product_category = ProductCategory.objects.get(slug=slug)
            old_instance = deepcopy(product_category)
            product_category.delete()
            self.log_entity_change(
                self.ctx,
                instance=old_instance,
                action=ActionType.DELETE,
                description=f"Product category '{old_instance.name}' deleted.",
            )
            return None
        except ProductCategory.DoesNotExist:
            return ServiceException(
                f"Product category with slug '{slug}' does not exist."
            )
        except Exception as e:
            return e
