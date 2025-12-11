"""
Product Service Module
Handles all business logic for product management operations.
"""

from copy import deepcopy
import logging
import os
from typing import Tuple, List, Optional, Sequence
from django.db.models.query import QuerySet
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Page
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.conf import settings

from core.enums.action_type import ActionType
from core.service import BaseService, required_context, ServiceException
from core.models import (
    Product,
    Brochure,
    ProductCategory,
    Specification,
    ProductSpecification,
)
from . import dto

logger = logging.getLogger(__name__)


class ProductService(BaseService):
    """Service class for managing product operations with comprehensive CRUD functionality."""

    def validate_slug_uniqueness(
        self, slug: str, exclude_id: Optional[int] = None
    ) -> bool:
        """
        Validate if slug is unique.

        Args:
            slug: The slug to validate
            exclude_id: Product ID to exclude from validation (for updates)

        Returns:
            True if slug is unique, False otherwise
        """
        queryset = Product.objects.filter(slug=slug)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return not queryset.exists()

    def validate_brochure_exists(self, brochure_id: int) -> bool:
        """
        Validate if brochure exists.

        Args:
            brochure_id: The brochure ID to validate

        Returns:
            True if brochure exists, False otherwise
        """
        return Brochure.objects.filter(id=brochure_id).exists()

    def validate_category_exists(self, category_slug: str) -> bool:
        """
        Validate if product category exists.

        Args:
            category_slug: The product category slug to validate

        Returns:
            True if product category exists, False otherwise
        """
        return ProductCategory.objects.filter(slug=category_slug).exists()

    @required_context
    def create_product(
        self, data: dto.CreateProductDTO
    ) -> Tuple[Product, Optional[Exception]]:
        """
        Create a new product with image and gallery handling.

        Args:
            data: Product creation data transfer object

        Returns:
            Tuple containing the created product and any error that occurred
        """
        try:
            # Validate slug uniqueness
            if data.slug and not self.validate_slug_uniqueness(data.slug):
                return Product(), ServiceException(
                    "Product with this slug already exists."
                )

            # Validate brochure exists if provided
            if data.brochure_id and not self.validate_brochure_exists(data.brochure_id):
                return Product(), ServiceException(
                    f"Brochure with id {data.brochure_id} does not exist."
                )

            product_data = data.to_dict()

            # Process main image upload
            if isinstance(data.image, InMemoryUploadedFile):
                product_data["image"] = data.image

            # Process gallery images upload
            if data.gallery:
                product_data["gallery"] = self._process_gallery_images(
                    data.gallery, data.slug
                )
            else:
                product_data["gallery"] = []

            # Handle brochure relationship
            product_data["brochure"] = (
                self._get_brochure_by_id(data.brochure_id) if data.brochure_id else None
            )
            product_data["category"] = (
                self._get_category_by_slug(data.category) if data.category else None
            )
            product_data.pop("brochure_id", None)

            product = Product.objects.create(**product_data)

            self.log_entity_change(
                self.ctx,
                product,
                action=ActionType.CREATE,
                description=f"Product '{product.name}' created.",
            )
            logger.info(f"Product created successfully with id {product.id}")
            return product, None

        except Exception as e:
            logger.error(f"Error creating product: {str(e)}", exc_info=True)
            return Product(), e

    def get_products(
        self, filters: Optional[dto.ProductFilterDTO] = None
    ) -> QuerySet[Product]:
        """
        Retrieve all products with optional filtering and optimized queries.

        Args:
            filters: Optional filter criteria for product search

        Returns:
            QuerySet of filtered and ordered products
        """
        queryset = Product.objects.select_related("brochure")

        if filters:
            # Use full-text search if specified (overrides basic search)
            if fulltext_search := filters.fulltext_search:
                return self._search_with_mysql_fulltext(queryset, fulltext_search)

            filter_conditions = Q()

            if filters.product_type:
                filter_conditions &= Q(product_type=filters.product_type)
            if filters.search:
                search_q = Q(name__icontains=filters.search) | Q(
                    description__icontains=filters.search
                )
                filter_conditions &= search_q
            if filters.is_active is not None:
                filter_conditions &= Q(is_active=filters.is_active)

            queryset = queryset.filter(filter_conditions)

        return queryset.order_by("-created_at")

    def get_paginated_products(
        self,
        str_page_number: str,
        str_page_size: str,
        filters: Optional[dto.ProductFilterDTO] = None,
    ) -> Page:
        """
        Retrieve paginated products with optional filtering.

        Args:
            str_page_number: Page number as string
            str_page_size: Page size as string
            filters: Optional filter criteria for product search

        Returns:
            Page object containing filtered and paginated products
        """
        queryset = self.get_products(filters)
        return self.get_paginated_data(queryset, str_page_number, str_page_size)

    def get_specific_product(self, pk: int) -> Tuple[Product, Optional[Exception]]:
        """
        Retrieve a specific product by its ID with optimized query.

        Args:
            pk: Product ID to retrieve

        Returns:
            Tuple containing the product and any error that occurred
        """
        try:
            product = Product.objects.select_related("brochure").get(id=pk)
            return product, None
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error retrieving product {pk}: {str(e)}", exc_info=True)
            return Product(), e

    def get_product_by_slug(self, slug: str) -> Tuple[Product, Optional[Exception]]:
        """
        Retrieve a product by its unique slug identifier.

        Args:
            slug: Product slug to search for

        Returns:
            Tuple containing the product and any error that occurred
        """
        try:
            product = Product.objects.select_related("brochure").get(slug=slug)
            return product, None
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_slug(slug)
        except Exception as e:
            logger.error(
                f"Error retrieving product by slug '{slug}': {str(e)}", exc_info=True
            )
            return Product(), e

    @required_context
    def update_specific_product(
        self, pk: int, data: dto.UpdateProductDTO
    ) -> Tuple[Product, Optional[Exception]]:
        """
        Update a specific product with comprehensive data handling.

        Args:
            pk: Product ID to update
            data: Product update data transfer object

        Returns:
            Tuple containing the updated product and any error that occurred
        """
        try:
            return self._update_product_with_data_handling(pk, data)
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error updating product {pk}: {str(e)}", exc_info=True)
            return Product(), e

    @required_context
    def delete_specific_product(self, pk: int) -> Optional[Exception]:
        """
        Delete a specific product and its associated files.

        Args:
            pk: Product ID to delete

        Returns:
            Exception if error occurs, None if successful
        """
        try:
            return self._delete_product_with_cleanup(pk)
        except Product.DoesNotExist:
            error_msg = f"Product with id '{pk}' does not exist."
            logger.warning(error_msg)
            return ServiceException(error_msg)
        except Exception as e:
            logger.error(f"Error deleting product {pk}: {str(e)}", exc_info=True)
            return e

    @required_context
    def toggle_product_status(
        self, pk: int, data: dto.ToggleProductStatusDTO
    ) -> Tuple[Product, Optional[Exception]]:
        """
        Toggle product active status efficiently.

        Args:
            pk: Product ID to update
            data: Status toggle data transfer object

        Returns:
            Tuple containing the updated product and any error that occurred
        """
        try:
            return self._toggle_product_status_with_logging(pk, data)
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error toggling product {pk} status: {str(e)}", exc_info=True)
            return Product(), e

    @required_context
    def update_product_image(
        self, pk: int, data: dto.UpdateProductImageDTO
    ) -> Tuple[Product, Optional[Exception]]:
        """
        Update product main image with automatic cleanup.

        Args:
            pk: Product ID to update
            data: Image update data transfer object

        Returns:
            Tuple containing the updated product and any error that occurred
        """
        try:
            return self._update_product_image_with_cleanup(pk, data)
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error updating product {pk} image: {str(e)}", exc_info=True)
            return Product(), e

    @required_context
    def update_product_gallery(
        self, pk: int, data: dto.UpdateProductGalleryDTO
    ) -> Tuple[Product, Optional[Exception]]:
        """
        Update product gallery images with automatic cleanup.

        Args:
            pk: Product ID to update
            data: Gallery update data transfer object

        Returns:
            Tuple containing the updated product and any error that occurred
        """
        try:
            return self._update_product_gallery_with_cleanup(pk, data)
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_id(pk)
        except Exception as e:
            logger.error(
                f"Error updating product {pk} gallery: {str(e)}", exc_info=True
            )
            return Product(), e

    @required_context
    def delete_product_gallery_image(
        self, pk: int, index: int
    ) -> Tuple[Product, Optional[Exception]]:
        """
        Delete a specific image from product gallery by index.

        Args:
            pk: Product ID
            index: Index of the gallery image to delete

        Returns:
            Tuple containing the updated product and any error that occurred
        """
        try:
            return self._delete_gallery_image_by_index(pk, index)
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_id(pk)
        except Exception as e:
            logger.error(
                f"Error deleting gallery image from product {pk}: {str(e)}",
                exc_info=True,
            )
            return Product(), e

    # Helper Methods for Internal Operations

    def _process_gallery_images(
        self, gallery_images: Sequence[InMemoryUploadedFile | str], slug: str
    ) -> List[str]:
        """
        Process gallery images and return list of saved paths.

        Args:
            gallery_images: List of image files or existing paths
            slug: Product slug for filename generation

        Returns:
            List of saved gallery image paths
        """
        gallery_paths = []
        for i, gallery_image in enumerate(gallery_images):
            if isinstance(gallery_image, InMemoryUploadedFile):
                gallery_path = self._save_product_gallery_image(gallery_image, slug, i)
                gallery_paths.append(gallery_path)
            elif isinstance(gallery_image, str):
                gallery_paths.append(gallery_image)
        return gallery_paths

    def _get_brochure_by_id(self, brochure_id: int) -> Optional[Brochure]:
        """
        Retrieve brochure by ID with error handling.

        Args:
            brochure_id: Brochure ID to retrieve

        Returns:
            Brochure instance or None if not found
        """
        try:
            return Brochure.objects.get(id=brochure_id)
        except Brochure.DoesNotExist:
            logger.warning(f"Brochure with id {brochure_id} not found")
            return None

    def _get_category_by_slug(self, category_slug: str) -> Optional[ProductCategory]:
        """
        Retrieve product category by slug with error handling.

        Args:
            category_slug: Product category slug to retrieve

        Returns:
            ProductCategory instance or None if not found
        """
        try:
            return ProductCategory.objects.get(slug=category_slug)
        except ProductCategory.DoesNotExist:
            logger.warning(f"Product category with slug '{category_slug}' not found")
            return None

    def _update_product_fields(self, product: Product, update_data: dict) -> None:
        """
        Update product fields with provided data.

        Args:
            product: Product instance to update
            update_data: Dictionary of fields to update
        """
        for key, value in update_data.items():
            if value is not None:
                setattr(product, key, value)

    def _cleanup_old_gallery_images(self, gallery_paths: List[str]) -> None:
        """
        Clean up old gallery image files from storage.

        Args:
            gallery_paths: List of gallery image paths to delete
        """
        if gallery_paths:
            for image_path in gallery_paths:
                self._delete_product_file(image_path)

    def _save_product_gallery_image(
        self, image: InMemoryUploadedFile, slug: str, index: int
    ) -> str:
        """
        Save product gallery image to storage with proper naming.

        Args:
            image: Uploaded image file
            slug: Product slug for filename generation
            index: Gallery image index for uniqueness

        Returns:
            Path to saved image file

        Raises:
            Exception: If image saving fails
        """
        try:
            file_extension = os.path.splitext(image.name)[1]
            filename = f"{slug}_gallery_{index}{file_extension}"
            file_path = (
                f"{settings.FILE_UPLOAD_BASE_DIR}uploads/products/gallery/{filename}"
            )

            saved_path = default_storage.save(file_path, image)
            logger.info(f"Product gallery image saved to {saved_path}")
            return saved_path

        except Exception as e:
            logger.error(f"Error saving product gallery image: {str(e)}", exc_info=True)
            raise ServiceException(f"Failed to save gallery image: {str(e)}") from e

    def _delete_product_file(self, file_path: str) -> None:
        """
        Delete product file from storage with error handling.

        Args:
            file_path: Path to file to delete
        """
        try:
            if file_path and default_storage.exists(file_path):
                default_storage.delete(file_path)
                logger.info(f"Product file {file_path} deleted successfully")
        except Exception as e:
            logger.warning(f"Error deleting product file {file_path}: {str(e)}")

    def _handle_product_not_found_by_id(
        self, pk: int
    ) -> Tuple[Product, ServiceException]:
        """
        Handle Product.DoesNotExist exception for ID-based lookups.

        Args:
            pk: Product ID that was not found

        Returns:
            Tuple containing empty Product and exception
        """
        return self._create_product_not_found_error("Product with id '", pk)

    def _handle_product_not_found_by_slug(
        self, slug: str
    ) -> Tuple[Product, ServiceException]:
        """
        Handle Product.DoesNotExist exception for slug-based lookups.

        Args:
            slug: Product slug that was not found

        Returns:
            Tuple containing empty Product and exception
        """
        return self._create_product_not_found_error("Product with slug '", slug)

    def _save_and_log_success(
        self, product: Product, field_name: str, pk: int, success_message: str
    ) -> Tuple[Product, None]:
        """
        Save product with specific field update and log success message.

        Args:
            product: Product instance to save
            field_name: Field name to include in update_fields
            pk: Product ID for logging
            success_message: Success message to log

        Returns:
            Tuple containing saved product and None
        """
        product.save(update_fields=[field_name, "updated_at"])
        logger.info(f"Product {pk} {success_message}")
        return product, None

    @required_context
    def _delete_product_with_cleanup(self, pk: int) -> None:
        """
        Delete product and clean up associated files.

        Args:
            pk: Product ID to delete

        Returns:
            None if successful
        """
        product = Product.objects.get(id=pk)

        # Clean up associated files
        if product.image:
            product.image.delete(save=False)
        if product.gallery:
            self._cleanup_old_gallery_images(product.gallery)

        product.delete()

        self.log_entity_change(
            self.ctx,
            product,
            action=ActionType.DELETE,
            description=f"Product '{product.name}' deleted.",
        )
        logger.info(f"Product {pk} deleted successfully")
        return None

    @required_context
    def _update_product_with_data_handling(
        self, pk: int, data: dto.UpdateProductDTO
    ) -> Tuple[Product, None]:
        """
        Update product with comprehensive data handling including images and relationships.

        Args:
            pk: Product ID to update
            data: Product update data transfer object

        Returns:
            Tuple containing the updated product and None
        """
        product = Product.objects.get(id=pk)
        old_instance = deepcopy(product)

        # Validate slug uniqueness if slug is being updated
        if data.slug and not self.validate_slug_uniqueness(data.slug, exclude_id=pk):
            raise ServiceException("Product with this slug already exists.")

        # Validate brochure exists if provided
        if data.brochure_id and not self.validate_brochure_exists(data.brochure_id):
            raise ServiceException(
                f"Brochure with id {data.brochure_id} does not exist."
            )

        if data.category and not self.validate_category_exists(data.category):
            raise ServiceException(
                f"Product category with slug '{data.category}' does not exist."
            )

        update_data = data.to_dict()

        # Handle main image update
        if isinstance(data.image, InMemoryUploadedFile):
            if product.image:
                product.image.delete(save=False)
            update_data["image"] = data.image

        # Handle gallery update
        if data.gallery:
            self._cleanup_old_gallery_images(product.gallery)
            update_data["gallery"] = self._process_gallery_images(
                data.gallery, data.slug or product.slug
            )

        # Handle brochure relationship update
        if data.brochure_id:
            update_data["brochure"] = self._get_brochure_by_id(data.brochure_id)

        if data.category:
            update_data["category"] = self._get_category_by_slug(data.category)

        update_data.pop("brochure_id", None)

        # Apply updates to product
        self._update_product_fields(product, update_data)
        product.save()

        self.log_entity_change(
            self.ctx,
            product,
            old_instance=old_instance,
            action=ActionType.UPDATE,
            description=f"Product '{product.name}' updated.",
        )
        logger.info(f"Product {pk} updated successfully")
        return product, None

    @required_context
    def _toggle_product_status_with_logging(
        self, pk: int, data: dto.ToggleProductStatusDTO
    ) -> Tuple[Product, None]:
        """
        Toggle product status and log the action.

        Args:
            pk: Product ID to update
            data: Status toggle data transfer object

        Returns:
            Tuple containing the updated product and None
        """
        product = Product.objects.get(id=pk)
        old_instance = deepcopy(product)

        product.is_active = data.is_active
        product.save(update_fields=["is_active", "updated_at"])

        status_text = "activated" if data.is_active else "deactivated"
        self.log_entity_change(
            self.ctx,
            product,
            old_instance=old_instance,
            action=ActionType.UPDATE,
            description=(f"Product '{product.name}' has been {status_text}."),
        )
        logger.info(f"Product {pk} {status_text} successfully")
        return product, None

    @required_context
    def _update_product_image_with_cleanup(
        self, pk: int, data: dto.UpdateProductImageDTO
    ) -> Tuple[Product, None]:
        """
        Update product image with cleanup of old image.

        Args:
            pk: Product ID to update
            data: Image update data transfer object

        Returns:
            Tuple containing the updated product and None
        """
        product = Product.objects.get(id=pk)
        old_instance = deepcopy(product)

        # Clean up old image
        if product.image:
            product.image.delete(save=False)

        # Save new image
        product.image.save(data.image.name, data.image, save=False)
        product, err = self._save_and_log_success(
            product, "image", pk, "main image updated successfully"
        )

        self.log_entity_change(
            self.ctx,
            product,
            old_instance=old_instance,
            action=ActionType.UPDATE,
            description=f"Product '{product.name}' image updated.",
        )
        return product, err

    @required_context
    def _update_product_gallery_with_cleanup(
        self, pk: int, data: dto.UpdateProductGalleryDTO
    ) -> Tuple[Product, None]:
        """
        Update product gallery with cleanup of old images.

        Args:
            pk: Product ID to update
            data: Gallery update data transfer object

        Returns:
            Tuple containing the updated product and None
        """
        product = Product.objects.get(id=pk)
        old_instance = deepcopy(product)

        # Clean up old gallery images
        if product.gallery:
            self._cleanup_old_gallery_images(product.gallery)

        # Save new gallery images
        product.gallery = self._process_gallery_images(data.gallery, product.slug)
        product, err = self._save_and_log_success(
            product, "gallery", pk, "gallery updated successfully"
        )

        self.log_entity_change(
            self.ctx,
            product,
            old_instance=old_instance,
            action=ActionType.UPDATE,
            description=f"Product '{product.name}' gallery updated.",
        )
        return product, err

    @required_context
    def _delete_gallery_image_by_index(
        self, pk: int, index: int
    ) -> Tuple[Product, None]:
        """
        Delete a specific gallery image by index with validation.

        Args:
            pk: Product ID
            index: Index of the gallery image to delete

        Returns:
            Tuple containing the updated product and None

        Raises:
            Exception: If gallery image at index does not exist
        """
        product = Product.objects.get(id=pk)
        old_instance = deepcopy(product)

        if not product.gallery or index >= len(product.gallery) or index < 0:
            error_msg = (
                f"Gallery image at index {index} does not exist for product {pk}."
            )
            logger.warning(error_msg)
            raise ServiceException(error_msg)

        # Delete the specific image file
        self._delete_product_file(product.gallery[index])

        # Remove from gallery list
        product.gallery = [img for i, img in enumerate(product.gallery) if i != index]
        product.save(update_fields=["gallery", "updated_at"])

        self.log_entity_change(
            self.ctx,
            product,
            old_instance=old_instance,
            action=ActionType.UPDATE,
            description=f"Gallery image at index {index} deleted from product {pk}.",
        )
        logger.info(f"Gallery image at index {index} deleted from product {pk}")
        return product, None

    def _search_with_mysql_fulltext(
        self, queryset: QuerySet[Product], query: str
    ) -> QuerySet[Product]:
        """
        Perform MySQL full-text search across product and product variant fields.

        Uses MySQL's MATCH...AGAINST with NATURAL LANGUAGE MODE for efficient
        full-text searching. Searches across:
        - Product: name, description
        - ProductVariant: model, description

        Results are ordered by relevance score and creation date.

        Note: Requires FULLTEXT index on searched fields in database schema.

        Args:
            queryset: Base queryset to apply search filter on
            query: Search term(s) to find in product content

        Returns:
            QuerySet[Product]: Filtered queryset ordered by relevance and date
        """
        if not query or not query.strip():
            return queryset

        # Escape single quotes for SQL safety (params handle injection prevention)
        safe_query = query.strip().replace("'", "''")

        # Subquery untuk mencari di product_variants
        variant_subquery = """
            SELECT DISTINCT pv.product_id
            FROM product_variants pv
            WHERE MATCH(pv.model, pv.description)
            AGAINST (%s IN NATURAL LANGUAGE MODE)
        """

        return queryset.extra(
            select={
                "product_relevance": """
                    MATCH(name, description)
                    AGAINST (%s IN NATURAL LANGUAGE MODE)
                """,
            },
            select_params=[safe_query],
            where=[
                f"""
                MATCH(products.name, products.description)
                AGAINST (%s IN NATURAL LANGUAGE MODE)
                OR products.id IN ({variant_subquery})
                """
            ],
            params=[safe_query, safe_query],
        ).order_by("-product_relevance", "-created_at")

    def _create_product_not_found_error(
        self, prefix: str, identifier: int | str
    ) -> Tuple[Product, ServiceException]:
        """
        Create a standardized product not found error with logging.

        Args:
            prefix: Error message prefix (e.g., "Product with id '", "Product with slug '")
            identifier: Product identifier (ID or slug)

        Returns:
            Tuple containing empty Product and exception
        """
        error_msg = f"{prefix}{identifier}' does not exist."
        logger.warning(error_msg)
        return Product(), ServiceException(error_msg)

    @required_context
    def add_or_update_specifications_to_product(
        self,
        product_id: int,
        specifications: List[dto.CreateProductSpecificationItemDTO],
    ) -> Tuple[Product, Optional[Exception]]:
        """
        Add specifications to a product.

        Args:
            product_id: ID of the product to add specifications to
            specifications: List of specification DTOs to add

        Returns:
            Tuple containing the updated product and any error that occurred
        """
        try:
            if err := self._validate_product_specifications(specifications):
                raise err

            product = Product.objects.get(id=product_id)

            spec_slugs = [spec_dto.slug for spec_dto in specifications]
            specifications_map = Specification.objects.in_bulk(
                spec_slugs, field_name="slug"
            )

            existing_product_specs = {
                (ps.specification.slug): ps
                for ps in ProductSpecification.objects.filter(
                    product=product, specification__slug__in=spec_slugs
                ).select_related("specification")
            }

            with transaction.atomic():
                for spec_dto in specifications:
                    specification = specifications_map[spec_dto.slug]
                    old_instance = existing_product_specs.get(spec_dto.slug)

                    spec, created = ProductSpecification.objects.update_or_create(
                        product=product,
                        specification=specification,
                        defaults={
                            "value": spec_dto.value,
                            "highlighted": spec_dto.highlighted,
                        },
                    )

                    self.log_entity_change(
                        self.ctx,
                        spec,
                        action=ActionType.CREATE if created else ActionType.UPDATE,
                        old_instance=old_instance,
                        description=(
                            f"Specification '{specification.label}' "
                            f"{'added to' if created else 'updated for'} product '{product.name}'."
                        ),
                    )
                return product, None

        except Product.DoesNotExist:
            return Product(), ServiceException(
                f"Product with id '{product_id}' does not exist."
            )
        except Exception as e:
            logger.error(
                f"Error adding specifications to product {product_id}: {str(e)}",
                exc_info=True,
            )
            return Product(), e

    def _validate_product_specifications(
        self,
        specifications: List[dto.CreateProductSpecificationItemDTO],
    ) -> Optional[Exception]:
        """
        Validate that all specifications exist in database.

        Args:
            specifications: List of specification DTOs to validate

        Returns:
            Exception if validation fails, None otherwise
        """
        # Get all slugs from specifications
        spec_slugs = [spec_dto.slug for spec_dto in specifications]

        # Query all slugs in one go
        existing_slugs = set(
            Specification.objects.filter(slug__in=spec_slugs).values_list(
                "slug", flat=True
            )
        )

        # Check for missing slugs
        for slug in spec_slugs:
            if slug not in existing_slugs:
                return ServiceException(
                    f"Specification with slug '{slug}' does not exist."
                )

    @required_context
    def remove_specifications_from_product(
        self, product_id: int, specification_slugs: List[str]
    ) -> Optional[Exception]:
        """
        Remove specifications from a product.

        Args:
            product_id: ID of the product to remove specifications from
            specification_slugs: List of specification slugs to remove
        Returns:
            Exception if error occurs, None if successful
        """
        try:
            product = Product.objects.get(id=product_id)

            with transaction.atomic():
                for slug in specification_slugs:
                    try:
                        product_spec = ProductSpecification.objects.get(
                            product=product,
                            specification__slug=slug,
                        )
                        product_spec.delete()

                        self.log_entity_change(
                            self.ctx,
                            product_spec,
                            action=ActionType.DELETE,
                            description=(
                                f"Specification '{slug}' removed from product '{product.name}'."
                            ),
                        )
                    except ProductSpecification.DoesNotExist:
                        logger.warning(
                            f"Specification '{slug}' not found for product '{product.name}'."
                        )
            return None

        except Product.DoesNotExist:
            return ServiceException(f"Product with id '{product_id}' does not exist.")
        except Exception as e:
            logger.error(
                f"Error removing specifications from product {product_id}: {str(e)}",
                exc_info=True,
            )
            return e
