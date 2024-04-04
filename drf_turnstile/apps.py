from django.apps import AppConfig


class DRFTurnstileConfig(AppConfig):
    name = 'drf_turnstile'
    verbose_name = 'DRF Turnstile'

    def ready(self):
        from .checks import turnstile_system_check # NOQA