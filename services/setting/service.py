import copy
from typing import Tuple
from django.db.models.manager import BaseManager
from django.utils.text import slugify

from core.service import BaseService, required_context
from core.models import Setting
from core.enums import ActionType


class SettingService(BaseService):
    """
    Service class for managing application settings
    """

    @required_context
    def create_setting(self, **setting_data) -> Tuple[Setting, Exception | None]:
        """
        Create a new application settings
        """
        slug = setting_data.get("slug") or slugify(setting_data.get("label", ""))
        setting_data["slug"] = slug

        if Setting.objects.filter(slug=slug).exists():
            return Setting(), Exception(f"Setting with slug '{slug}' already exists.")

        setting = Setting.objects.create(**setting_data), None
        self.log_entity_change(
            self.ctx,
            action=ActionType.CREATE,
            instance=setting[0],
            description=f"Created setting '{setting[0].label}'.",
        )
        return setting

    def get_all_settings(self) -> BaseManager[Setting]:
        """
        Retrieve all application settings
        """
        return Setting.objects.all()

    def get_setting_by_slug(self, slug: str) -> Setting | None:
        """
        Retrieve a specific setting by its slug
        """
        try:
            return Setting.objects.get(slug=slug)
        except Setting.DoesNotExist:
            return None

    @required_context
    def update_setting_by_slug(
        self, slug: str, **update_data
    ) -> Tuple[Setting, Exception | None]:
        """
        Update a specific setting by its slug
        """
        setting = self.get_setting_by_slug(slug)
        if not setting:
            return Setting(), Exception(f"Setting with slug '{slug}' does not exist.")

        old_setting = copy.deepcopy(setting)
        for key, value in update_data.items():
            setattr(setting, key, value)
        setting.save()
        self.log_entity_change(
            self.ctx,
            action=ActionType.UPDATE,
            instance=setting,
            old_instance=old_setting,
            description=f"Updated setting '{setting.label}'.",
        )
        return setting, None

    @required_context
    def delete_setting_by_slug(self, slug: str) -> Exception | None:
        """
        Delete a specific setting by its slug
        """
        setting = self.get_setting_by_slug(slug)
        if not setting:
            return Exception(f"Setting with slug '{slug}' does not exist.")

        old_setting = copy.deepcopy(setting)
        setting.delete()
        self.log_entity_change(
            self.ctx,
            action=ActionType.DELETE,
            instance=old_setting,
            description=f"Deleted setting '{old_setting.label}'.",
        )
        return None
