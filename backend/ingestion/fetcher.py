"""Generic rate-limited HTTP JSON client with retry. Reusable for any source."""
import time
from typing import Any, Optional

import requests
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

from . import config


class RetryableHTTPError(Exception):
    """Raised for 429/5xx so tenacity retries them."""


class RateLimitedClient:
    """requests.Session wrapper: min delay between calls + retry with backoff."""

    def __init__(self, delay_sec: float = config.REQUEST_DELAY_SEC) -> None:
        self.delay_sec = delay_sec
        self._last_call: float = 0.0
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)

    def _wait(self) -> None:
        elapsed = time.monotonic() - self._last_call
        if elapsed < self.delay_sec:
            time.sleep(self.delay_sec - elapsed)

    @retry(
        retry=retry_if_exception_type(
            (requests.ConnectionError, requests.Timeout, RetryableHTTPError)),
        stop=stop_after_attempt(config.MAX_RETRIES),
        wait=wait_exponential(multiplier=2, min=2, max=60),
        reraise=True,
    )
    def get_json(self, url: str, params: Optional[dict] = None) -> Any:
        """GET url and return parsed JSON. Raises on non-retryable 4xx."""
        self._wait()
        try:
            resp = self.session.get(url, params=params, timeout=config.TIMEOUT_SEC)
        finally:
            self._last_call = time.monotonic()
        if resp.status_code == 429 or resp.status_code >= 500:
            raise RetryableHTTPError(f"{resp.status_code} for {resp.url}")
        resp.raise_for_status()
        return resp.json()
