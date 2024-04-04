TEST_SECRET_KEYS = {
    "ALWAYS_PASSES": "1x0000000000000000000000000000000AA",  # Always passes
    "ALWAYS_FAILS": "2x0000000000000000000000000000000AA",  # Always fails
    "TOKEN_SPEND_ERROR": "3x0000000000000000000000000000000AA",  # Yields a "token already spend" error
}

Turnstile_API_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"