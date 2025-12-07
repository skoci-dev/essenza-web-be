import contextlib
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core"

    def ready(self):
        """
        Import authentication extensions when Django starts
        """
        with contextlib.suppress(ImportError):
            import utils.docs  # This will register our JWTAuthenticationScheme

        # Initialize system service app start time
        with contextlib.suppress(ImportError):
            from services import SystemService

            SystemService.initialize_start_time()
