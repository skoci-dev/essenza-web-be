from copy import deepcopy
from typing import Tuple
from django.db.models.manager import BaseManager

from core.enums import ActionType
from core.service import BaseService, required_context
from core.models import Menu, MenuItem


class MenuService(BaseService):
    """Service class for managing menu items."""

    def create_menu(self, data: dict) -> Tuple[Menu, Exception | None]:
        """Create a new menu."""
        try:
            menu = Menu.objects.create(**data)
            self.log_entity_change(
                self.ctx,
                instance=menu,
                action=ActionType.CREATE,
            )
            return menu, None
        except Exception as e:
            return Menu(), e

    def get_menus(self, tree: bool = False) -> BaseManager[Menu]:
        """Retrieve all menus."""
        queryset = Menu.objects.all().prefetch_related("items")

        if tree:
            queryset = queryset.prefetch_related("items__children")
        return queryset

    def get_specific_menu(self, id: int) -> Tuple[Menu, Exception | None]:
        """Retrieve a specific menu by its ID."""
        try:
            menu = Menu.objects.get(id=id)
            return menu, None
        except Menu.DoesNotExist:
            return Menu(), Exception(f"Menu with id '{id}' does not exist.")
        except Exception as e:
            return Menu(), e

    @required_context
    def update_specific_menu(
        self, id: int, data: dict
    ) -> Tuple[Menu, Exception | None]:
        """Update a specific menu by its ID."""
        try:
            menu = Menu.objects.get(id=id)
            old_instance = deepcopy(menu)
            for key, value in data.items():
                setattr(menu, key, value)
            menu.save()
            self.log_entity_change(
                self.ctx,
                instance=menu,
                old_instance=old_instance,
                action=ActionType.UPDATE,
            )
            return menu, None
        except Menu.DoesNotExist:
            return Menu(), Exception(f"Menu with id '{id}' does not exist.")
        except Exception as e:
            return Menu(), e

    @required_context
    def delete_specific_menu(self, id: int) -> Exception | None:
        """Delete a specific menu by its ID."""
        try:
            menu = Menu.objects.get(id=id)
            old_instance = deepcopy(menu)
            menu.delete()
            self.log_entity_change(
                self.ctx,
                instance=old_instance,
                action=ActionType.DELETE,
            )
            return None
        except Menu.DoesNotExist:
            return Exception(f"Menu with id '{id}' does not exist.")
        except Exception as e:
            return e

    def get_menu_items(
        self, menu_id: int
    ) -> Tuple[BaseManager[MenuItem], Exception | None]:
        """Retrieve all items for a specific menu."""
        try:
            menu = Menu.objects.get(id=menu_id)
            return MenuItem.objects.filter(menu=menu), None
        except Menu.DoesNotExist:
            return MenuItem.objects.none(), Exception(
                f"Menu with id '{menu_id}' does not exist."
            )
        except Exception as e:
            return MenuItem.objects.none(), e
