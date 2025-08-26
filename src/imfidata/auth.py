from __future__ import annotations

import os
from typing import Dict, List, Tuple

from msal import PublicClientApplication, SerializableTokenCache

# === CONFIGURATION (can be overridden by env vars) ===
CLIENT_ID  = os.getenv("IMFIDATA_CLIENT_ID", "446ce2fa-88b1-436c-b8e6-94491ca4f6fb")
AUTHORITY  = os.getenv(
    "IMFIDATA_AUTHORITY",
    "https://imfprdb2c.b2clogin.com/imfprdb2c.onmicrosoft.com/b2c_1a_signin_aad_simple_user_journey/",
)
SCOPE      = os.getenv(
    "IMFIDATA_SCOPE",
    "https://imfprdb2c.onmicrosoft.com/4042e178-3e2f-4ff9-ac38-1276c901c13d/iData.Login",
)
SCOPES: List[str] = [SCOPE]
CACHE_PATH = os.getenv("IMFIDATA_CACHE_PATH", "msal_token_cache.bin")


def _load_cache(path: str = CACHE_PATH) -> SerializableTokenCache:
    cache = SerializableTokenCache()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            cache.deserialize(f.read())
    return cache


def _persist_cache(cache: SerializableTokenCache, path: str = CACHE_PATH) -> None:
    if cache.has_state_changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(cache.serialize())


def build_app() -> Tuple[PublicClientApplication, SerializableTokenCache]:
    cache = _load_cache()
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
        token_cache=cache,
    )
    return app, cache


def acquire_access_token(scopes: List[str] = SCOPES) -> Dict[str, str]:
    """
    Acquire an OAuth2 access token using MSAL.
    Prefers silent auth (cached account) and falls back to interactive.
    """
    app, cache = build_app()
    accounts = app.get_accounts()
    result = app.acquire_token_silent(scopes, account=accounts[0]) if accounts else None
    if not result:
        result = app.acquire_token_interactive(scopes=scopes)
    _persist_cache(cache)
    if not result or "access_token" not in result:
        err = (result or {}).get("error_description", (result or {}).get("error", "unknown error"))
        raise RuntimeError(f"Failed to acquire token: {err}")
    return result


def get_request_header(needs_auth: bool = True) -> Dict[str, str]:
    """
    Return a standard header with optional Authorization.
    """
    headers = {"User-Agent": "imfidata-client"}
    if not needs_auth:
        return headers

    token_resp = acquire_access_token()
    token_type = token_resp.get("token_type", "Bearer")
    access_token = token_resp["access_token"]
    headers["Authorization"] = f"{token_type} {access_token}"
    return headers
