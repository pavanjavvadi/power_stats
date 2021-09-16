from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "power_stats.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import power_stats.users.signals  # noqa F401
        except ImportError:
            pass
