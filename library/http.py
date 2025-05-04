import httpx
from library.torbox import TORBOX_API_KEY

TORBOX_API_URL = "https://api.torbox.app/v1/api"
TORBOX_SEARCH_API_URL = "https://search-api.torbox.app"

api_http_client = httpx.Client(
    base_url=TORBOX_API_URL,
    headers={
        "Authorization": f"Bearer {TORBOX_API_KEY}",
        "User-Agent": "TorBox-Media-Center/1.0 TorBox/1.0",
    },
    timeout=httpx.Timeout(60),
    follow_redirects=True,
)

search_api_http_client = httpx.Client(
    base_url=TORBOX_SEARCH_API_URL,
    headers={
        "Authorization": f"Bearer {TORBOX_API_KEY}",
        "User-Agent": "TorBox-Media-Center/1.0 TorBox/1.0",
    },
    timeout=httpx.Timeout(60),
    follow_redirects=True,
)
