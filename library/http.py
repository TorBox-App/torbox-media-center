import httpx
from library.torbox import TORBOX_API_KEY

TORBOX_API_URL = "https://api.torbox.app/v1/api"
TORBOX_SEARCH_API_URL = "https://search-api.torbox.app"

transport = httpx.HTTPTransport(
    retries=10
)

api_http_client = httpx.Client(
    base_url=TORBOX_API_URL,
    headers={
        "Authorization": f"Bearer {TORBOX_API_KEY}",
        "User-Agent": "TorBox-Media-Center/1.0 TorBox/1.0",
    },
    timeout=httpx.Timeout(60),
    follow_redirects=True,
    transport=transport,
)

search_api_http_client = httpx.Client(
    base_url=TORBOX_SEARCH_API_URL,
    headers={
        "Authorization": f"Bearer {TORBOX_API_KEY}",
        "User-Agent": "TorBox-Media-Center/1.0 TorBox/1.0",
    },
    timeout=httpx.Timeout(60),
    follow_redirects=True,
    transport=transport,
)

general_http_client = httpx.Client(
    headers={
        "Authorization": f"Bearer {TORBOX_API_KEY}",
        "User-Agent": "TorBox-Media-Center/1.0 TorBox/1.0",
    },
    timeout=httpx.Timeout(60),
    follow_redirects=False,
    transport=transport,
)
