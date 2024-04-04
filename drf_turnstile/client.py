from datetime import datetime
from urllib.parse import urlencode
from urllib.request import ProxyHandler, Request, build_opener
from drf_turnstile.constants import Turnstile_API_URL
from django.conf import settings
import json


class TurnstileResponse:
    def __init__(self, success: bool, error_codes: list = None, challenge_ts: datetime = None, action: str = None
                 , cdata: str = None):
        self.success = success
        self.error_codes = error_codes or []
        self.challenge_ts = challenge_ts
        self.action = action
        self.cdata = cdata


def turnstile_request(params: bytes) -> any:
    request_object = Request(
        url="%s" % getattr(settings, 'DRF_TURNSTILE_URL', Turnstile_API_URL),
        data=params,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )

    opener_args = []
    proxies = getattr(settings, 'DRF_TURNSTILE_PROXIES', {})
    if proxies:
        opener_args = [ProxyHandler(proxies)]
    opener = build_opener(*opener_args)

    return opener.open(
        request_object,
        timeout=getattr(settings, 'DRF_TURNSTILE_TIMEOUT', 10),
    )


def submit(turnstile_response: str, secret_key: str, remoteip: str) -> TurnstileResponse:
    params = urlencode(
        {"secret": secret_key, "response": turnstile_response, "remoteip": remoteip}
    )

    params = params.encode('utf-8')

    response = turnstile_request(params)
    data = json.loads(response.read().decode("utf-8"))
    response.close()
    return TurnstileResponse(
        success=data.get('success'),
        error_codes=data.get('error-codes', None),
        challenge_ts=data.get('challenge_ts', None),
        action=data.get('action', None),
        cdata=data.get('cdata', None)
    )
