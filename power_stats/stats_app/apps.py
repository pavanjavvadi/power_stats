from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StatsAppConfig(AppConfig):
    name = 'power_stats.stats_app'
    verbose_name = _("StatsApp")

    def ready(self):
        try:
            import power_stats.stats_app.signals  # noqa F401
        except ImportError:
            pass
