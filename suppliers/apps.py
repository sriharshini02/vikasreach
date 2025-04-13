from django.apps import AppConfig


class SuppliersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "suppliers"

    def ready(self):
        import suppliers.signals  # noqa
