import httpx
from library.torbox import TORBOX_API_KEY
from library.app import getCurrentVersion
import time
import logging
import hashlib
import json

TORBOX_API_URL = "https://api.torbox.app/v1/api"
TORBOX_SEARCH_API_URL = "https://search-api.torbox.app"
USER_AGENT = f"TorBox-Media-Center/{getCurrentVersion()} TorBox/1.0"
CACHE_TTL = 300 # cache time-to-live in seconds
_cache: dict[str, tuple[float, httpx.Response]] = {}

def makeCacheKey(method: str, url: str, base_url: str, **kwargs) -> str:
    key_data = {
        "method": method,
        "url": url,
        "base_url": base_url,
        "params": kwargs.get("params"),
        "json": kwargs.get("json"),
        "data": kwargs.get("data"),
    }
    key_str = json.dumps(key_data, sort_keys=True, default=str)
    return hashlib.sha256(key_str.encode()).hexdigest()

transport = httpx.HTTPTransport(
    retries=10
)

api_http_client = httpx.Client(
    base_url=TORBOX_API_URL,
    headers={
        "Authorization": f"Bearer {TORBOX_API_KEY}",
        "User-Agent": USER_AGENT,
    },
    timeout=httpx.Timeout(60),
    follow_redirects=True,
    transport=transport
)

search_api_http_client = httpx.Client(
    base_url=TORBOX_SEARCH_API_URL,
    headers={
        "Authorization": f"Bearer {TORBOX_API_KEY}",
        "User-Agent": USER_AGENT,
    },
    timeout=httpx.Timeout(60),
    follow_redirects=True,
    transport=transport,
)

general_http_client = httpx.Client(
    headers={
        "Authorization": f"Bearer {TORBOX_API_KEY}",
        "User-Agent": USER_AGENT,
    },
    timeout=httpx.Timeout(60),
    follow_redirects=False,
    transport=transport,
)


def requestWrapper(client: httpx.Client, method: str, url: str, use_cache: bool = True, **kwargs) -> httpx.Response:
    max_retries = 5
    backoff_factor = 1.5
    
    cacheable = use_cache and method.upper() == "GET" # only caching GET requests
    cache_key = None
    
    if cacheable:
        cache_key = makeCacheKey(method, url, str(client.base_url), **kwargs)
        if cache_key in _cache:
            cached_time, cached_response = _cache[cache_key]
            if time.time() - cached_time < CACHE_TTL:
                logging.debug(f"Cache hit for {url}")
                return cached_response
            else:
                del _cache[cache_key]
    
    for attempt in range(max_retries):
        try:
            response = client.request(method, url, **kwargs)
            response.raise_for_status()
            
            if cacheable and cache_key:
                _cache[cache_key] = (time.time(), response)
                logging.debug(f"Cached response for {url}")
            
            return response
        except httpx.HTTPStatusError as e:
            if e.response.has_redirect_location:
                if cacheable and cache_key:
                    _cache[cache_key] = (time.time(), e.response)
                    logging.debug(f"Cached redirect response for {url}")
                return e.response

            bad_response_codes = [429]
            if e.response.status_code in bad_response_codes:
                wait_time = backoff_factor * (2 ** attempt)
                logging.warning(f"Received {e.response.status_code} for {url}. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                logging.error(f"HTTP error for {url}: {e}")
                raise
        except httpx.RequestError as e:
            wait_time = backoff_factor * (2 ** attempt)
            logging.warning(f"Request error on {url}: {e}. Retrying in {wait_time:.2f} seconds...")
            time.sleep(wait_time)
    raise httpx.RequestError(f"Failed to complete request to {url} after {max_retries} attempts.")
