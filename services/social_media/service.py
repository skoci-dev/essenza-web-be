from typing import Tuple
from django.core.paginator import Page

from core.enums import ActionType
from core.service import BaseService, required_context
from core.models import SocialMedia


class SocialMediaService(BaseService):
    """
    Service class for managing social media entities and operations
    """

    SOCIAL_MEDIA_NOT_FOUND_ERROR = "Social media entry not found"

    def get_social_media_list(
        self, str_page_number: str = "1", str_page_size: str = "20"
    ) -> Page:
        """
        Retrieve a paginated list of social media entries ordered by order_no and created_at
        """
        queryset = SocialMedia.objects.order_by("order_no", "-created_at")
        return self.get_paginated_data(queryset, str_page_number, str_page_size)

    @required_context
    def create_social_media(self, **data) -> SocialMedia:
        """
        Create a new social media entry with the provided data
        """
        result = SocialMedia.objects.create(**data)
        self.log_entity_change(
            self.ctx,
            result,
            action=ActionType.CREATE,
            description=f"Created social media entry: {result.platform}",
        )
        return result

    def get_social_media_by_id(
        self, pk: int
    ) -> Tuple[SocialMedia | None, Exception | None]:
        """
        Retrieve a specific social media entry by its primary key
        """
        try:
            socmed = SocialMedia.objects.get(pk=pk)
            return socmed, None
        except SocialMedia.DoesNotExist:
            return None, Exception(self.SOCIAL_MEDIA_NOT_FOUND_ERROR)
        except Exception as e:
            return None, e

    @required_context
    def update_social_media(
        self, pk: int, **data
    ) -> Tuple[SocialMedia | None, Exception | None]:
        """
        Update an existing social media entry identified by pk with the provided data
        """
        try:
            socmed = SocialMedia.objects.get(pk=pk)
            for key, value in data.items():
                setattr(socmed, key, value)
            socmed.save()
            self.log_entity_change(
                self.ctx,
                socmed,
                action=ActionType.UPDATE,
                description=f"Updated social media entry: {socmed.platform}",
            )
            return socmed, None
        except SocialMedia.DoesNotExist:
            return None, Exception(self.SOCIAL_MEDIA_NOT_FOUND_ERROR)
        except Exception as e:
            return None, e

    @required_context
    def delete_social_media(self, pk: int) -> Exception | None:
        """
        Delete a specific social media entry by its primary key
        """
        try:
            socmed = SocialMedia.objects.get(pk=pk)
            socmed.delete()
            self.log_entity_change(
                self.ctx,
                socmed,
                action=ActionType.DELETE,
                description=f"Deleted social media entry: {socmed.platform}",
            )
            return None
        except SocialMedia.DoesNotExist:
            return Exception(self.SOCIAL_MEDIA_NOT_FOUND_ERROR)
        except Exception as e:
            return e
