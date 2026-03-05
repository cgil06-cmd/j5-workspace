#!/usr/bin/env python3
"""
lib/utils.py — Shared utilities for J5 agents
"""
import time
import urllib.error


def with_retry(fn, max_attempts=3, backoff=None, retryable_codes=(429, 500, 502, 503, 504, 529)):
    """
    Retry fn() up to max_attempts times with exponential backoff.

    - On urllib HTTPError with retryable code: wait and retry
    - On urllib HTTPError with non-retryable 4xx: raise immediately, no retry
    - On network/other errors: wait and retry
    - Returns result of fn() on success
    - Raises last exception if all attempts exhausted
    """
    if backoff is None:
        backoff = [1, 3, 7]

    last_exc = None
    for attempt in range(max_attempts):
        try:
            return fn()
        except urllib.error.HTTPError as e:
            last_exc = e
            code = e.code
            if code in retryable_codes:
                wait = backoff[attempt] if attempt < len(backoff) else backoff[-1]
                print(f"[utils] HTTP {code} on attempt {attempt + 1}/{max_attempts}, retrying in {wait}s")
                time.sleep(wait)
            elif 400 <= code < 500:
                # Non-retryable client error
                raise
            else:
                wait = backoff[attempt] if attempt < len(backoff) else backoff[-1]
                print(f"[utils] HTTP {code} on attempt {attempt + 1}/{max_attempts}, retrying in {wait}s")
                time.sleep(wait)
        except Exception as e:
            last_exc = e
            wait = backoff[attempt] if attempt < len(backoff) else backoff[-1]
            print(f"[utils] Error on attempt {attempt + 1}/{max_attempts}: {e}, retrying in {wait}s")
            time.sleep(wait)

    raise last_exc
