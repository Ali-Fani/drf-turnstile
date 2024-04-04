from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.serializers import ValidationError
from urllib.error import HTTPError
from drf_turnstile.client import TurnstileResponse
import logging
from ipware import get_client_ip
from drf_turnstile import client

logger = logging.getLogger(__name__)


class TurnstileValidator:
    requires_context = True

    messages = {
        "captcha_invalid": "Error verifying turnstile, please try again.",
        "captcha_error": "Error verifying turnstile, please try again.",
    }
    default_turnstile_secret_key = ""

    def __call__(self, value, serializer_field):
        if self._is_testing():
            self._run_validation_as_testing()
            return

        turnstile_secret_key = self._get_secret_key_from_context_or_default(
            serializer_field
        )
        client_ip = self._get_client_ip_from_context(serializer_field)
        check_captcha = self._get_captcha_response_with_payload(
            value=value,
            secret_key=turnstile_secret_key,
            client_ip=client_ip,
        )

        self._pre_validate_response(check_captcha)
        self._process_response(check_captcha)

    @staticmethod
    def _is_testing() -> bool:
        return getattr(settings, "DRF_TURNSTILE_TESTING", False)

    def _run_validation_as_testing(self):
        testing_result = getattr(settings, "DRF_TURNSTILE_TESTING_RESULT", True)
        if not testing_result:
            raise ValidationError(
                self.messages["captcha_invalid"], code="captcha_invalid"
            )

    def _get_secret_key_from_context_or_default(self, serializer_field) -> str:
        return serializer_field.context.get(
            "DRF_TURNSTILE_SECRET_KEY", self.default_turnstile_secret_key
        )

    @staticmethod
    def _get_client_ip_from_context(serializer_field):
        request = serializer_field.context.get("request")
        if not request:
            raise ImproperlyConfigured(
                "Couldn't get client ip address. Check your serializer gets context with request."
            )

        recaptcha_client_ip, _ = get_client_ip(request)
        return recaptcha_client_ip

    def _get_captcha_response_with_payload(self, value: str, secret_key: str, client_ip: str) -> TurnstileResponse:
        try:
            check_captcha = client.submit(
                turnstile_response=value,
                secret_key=secret_key,
                remoteip=client_ip
            )
        except HTTPError:
            logger.exception("Error verifying turnstile")
            raise ValidationError(
                self.messages["captcha_error"], code="captcha_error"
            )
        return check_captcha

    def _pre_validate_response(self, check_captcha: TurnstileResponse):
        if check_captcha.success:
            return

        logger.error(
            "Turnstile validation failed: %s", check_captcha.error_codes
        )

        raise ValidationError(
            self.messages["captcha_invalid"], code="captcha_invalid"
        )

    def _process_response(self, check_captcha: TurnstileResponse):
        ...


class TurnstileV0Validator(TurnstileValidator):
    def __init__(self, action: str, secret_key: str):
        self.turnstile_action = action
        self.default_turnstile_secret_key = secret_key

    def _process_response(self, check_captcha: TurnstileResponse):
        action = check_captcha.action or None
        if self.turnstile_action != action:
            logger.error(
                "Turnstile action mismatch: %s != %s", self.turnstile_action, action
            )
            raise ValidationError(
                self.messages["captcha_invalid"], code="captcha_invalid"
            )
