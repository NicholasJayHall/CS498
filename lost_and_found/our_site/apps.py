from django.apps import AppConfig


class OurSiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'our_site'

    def ready(self):
        import our_site.signals  # noqa: F401 – connect signal handlers
