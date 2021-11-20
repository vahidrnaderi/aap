"""Account apps config."""
from django.apps import AppConfig
from django.db.utils import OperationalError


class AuthConfig(AppConfig):
    """Django built-in class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "account"

    def ready(self):
        """Add 'external' content type."""
        from django.contrib.contenttypes.models import ContentType

        try:
            ContentType.objects.get_or_create(app_label="external", model="")
        except OperationalError:
            pass
