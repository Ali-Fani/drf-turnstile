from rest_framework.serializers import CharField
from django.conf import settings
from drf_turnstile.validators import TurnstileV0Validator


class TurnstileV0Field(CharField):
    def __init__(self, action: str, secret_key: str = None, **kwargs):
        super().__init__(**kwargs)

        self.write_only = True

        secret_key = secret_key or settings.DRF_TURNSTILE_SECRET_KEY

        validator = TurnstileV0Validator(secret_key=secret_key, action=action)
        self.validators.append(validator)
