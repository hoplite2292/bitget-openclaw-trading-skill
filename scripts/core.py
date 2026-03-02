import base64
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from urllib import error, parse, request

BASE_URL = "https://api.bitget.com"
DEFAULT_TIMEOUT = 10


class BitgetApiError(RuntimeError):
    """Raised when Bitget API returns an error or request fails."""


def _resolve_env_path() -> Path | None:
    override_path = os.getenv("BITGET_ENV_FILE")
    if override_path:
        path = Path(override_path).expanduser()
        if path.exists() and path.is_file():
            return path

    candidates = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent / ".env",
        Path(__file__).resolve().parent.parent / ".env",
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def load_dotenv() -> None:
    """Load .env file into process environment without overriding existing vars."""
    env_path = _resolve_env_path()
    if env_path is None:
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def _timestamp_ms() -> str:
    return str(int(time.time() * 1000))


def _compact_json(payload: Mapping[str, Any] | None) -> str:
    if payload is None:
        return ""
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)


def _query_string(query: Mapping[str, Any] | None) -> str:
    if not query:
        return ""

    pairs: list[tuple[str, str]] = []
    for key, value in query.items():
        if value is None:
            continue
        pairs.append((key, str(value)))

    if not pairs:
        return ""

    return "?" + parse.urlencode(pairs)


@dataclass
class BitgetClient:
    api_key: str
    secret_key: str
    passphrase: str
    base_url: str = BASE_URL
    timeout: int = DEFAULT_TIMEOUT

    @classmethod
    def from_env(cls) -> "BitgetClient":
        load_dotenv()

        api_key = os.getenv("BITGET_API_KEY", "").strip()
        secret_key = os.getenv("BITGET_SECRET_KEY", "").strip()
        passphrase = os.getenv("BITGET_PASSPHRASE", "").strip()

        missing: list[str] = []
        if not api_key:
            missing.append("BITGET_API_KEY")
        if not secret_key:
            missing.append("BITGET_SECRET_KEY")
        if not passphrase:
            missing.append("BITGET_PASSPHRASE")

        if missing:
            raise BitgetApiError(
                "Missing required environment variables: " + ", ".join(missing)
            )

        return cls(api_key=api_key, secret_key=secret_key, passphrase=passphrase)

    def _sign(
        self,
        timestamp: str,
        method: str,
        request_path: str,
        query_string: str,
        body: str,
    ) -> str:
        pre_hash = f"{timestamp}{method.upper()}{request_path}{query_string}{body}"
        digest = hmac.new(
            self.secret_key.encode("utf-8"),
            pre_hash.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        return base64.b64encode(digest).decode("utf-8")

    def request(
        self,
        method: str,
        request_path: str,
        query: Mapping[str, Any] | None = None,
        body: Mapping[str, Any] | None = None,
    ) -> Mapping[str, Any] | list[Any] | str:
        method_up = method.upper()
        query_str = _query_string(query)
        body_str = _compact_json(body)
        timestamp = _timestamp_ms()

        signature = self._sign(
            timestamp=timestamp,
            method=method_up,
            request_path=request_path,
            query_string=query_str,
            body=body_str,
        )

        url = f"{self.base_url}{request_path}{query_str}"
        headers = {
            "Content-Type": "application/json",
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
        }

        data = None
        if method_up in {"POST", "PUT", "DELETE"}:
            data = body_str.encode("utf-8") if body_str else b""

        req = request.Request(url=url, data=data, headers=headers, method=method_up)

        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
        except error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise BitgetApiError(f"HTTP {exc.code}: {details}") from exc
        except error.URLError as exc:
            raise BitgetApiError(f"Network error: {exc.reason}") from exc

        if not raw:
            return ""

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            return raw

        if isinstance(payload, dict):
            code = payload.get("code")
            if code not in (None, "00000"):
                message = payload.get("msg") or payload.get("message") or "Unknown error"
                raise BitgetApiError(f"Bitget API error {code}: {message}")

        return payload


def print_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
