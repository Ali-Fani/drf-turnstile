from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from typing import Any, List, Optional
from django.apps import AppConfig


def turnstile_system_check(app_configs: Optional[List[AppConfig]], **kwargs: Any) -> List:
    errors = []

    is_testing = getattr(settings, 'DRF_TURNSTILE_TESTING', False)
    if is_testing:
        return errors

    secret_key = getattr(settings, 'DRF_TURNSTILE_SECRET_KEY', None)
    if not secret_key:
        raise ImproperlyConfigured('DRF_TURNSTILE_SECRET_KEY is required')

    return errors
