SECRET_KEY = "TEST_SECRET_KEY"

INSTALLED_APPS = [
    "drf_turnstile",
]

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "test.sqlite3"}
}

DRF_TURNSTILE_SECRET_KEY = "TEST_DRF_TURNSTILE_SECRET_KEY"
