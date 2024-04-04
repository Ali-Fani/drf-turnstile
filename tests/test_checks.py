import pytest
from django.core.exceptions import ImproperlyConfigured

from drf_turnstile.checks import turnstile_system_check
from drf_turnstile.constants import TEST_SECRET_KEYS


def test_warning_no_secret_key(settings):
    settings.DRF_TURNSTILE_SECRET_KEY = None

    with pytest.raises(ImproperlyConfigured) as exc_info:
        turnstile_system_check(None)

    assert str(exc_info.value) == "settings.DRF_Turnstile_SECRET_KEY must be set."


def test_silent_testing(settings):
    settings.DRF_TURNSTILE_TESTING = True
    settings.DRF_TURNSTILE_SECRET_KEY = None

    assert turnstile_system_check(None) == []


def test_warning_test_secret_key(settings):
    settings.DRF_RECAPTCHA_SECRET_KEY = TEST_SECRET_KEYS[0]

    errors = turnstile_system_check(None)
    assert len(errors) == 1
    assert errors[0].hint == "Update settings.DRF_TURNSTILE_SECRET_KEY"
