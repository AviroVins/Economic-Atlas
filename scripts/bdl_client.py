"""Cienki klient API BDL (GUS): ponowienia przy 429, pauza między zapytaniami, stronicowanie.

Endpointy i nazwy parametrów trzeba potwierdzić w oficjalnej dokumentacji GUS
(https://bdl.stat.gov.pl/api/v1/swagger) - to część wymagań Lab 2.
"""
from __future__ import annotations

import re
import os
import time
import requests

from datetime import datetime, timezone


BASE_URL = "https://bdl.stat.gov.pl/api/v1"


def _retry_after_seconds(value: str | None, attempt: int) -> float:
    """GUS zwraca np. '140 sek'; standardowo byłoby samo '140'. Przy nieznanym formacie: backoff."""
    if value:
        m = re.fullmatch(r"\s*(\d+(?:[.,]\d+)?)\s*(?:s|sek\w*|sec\w*)?\s*", value, re.I)
        if m:
            return float(m.group(1).replace(",", "."))
    return float(2 ** attempt * 2)

class BdlClient:
    def __init__(self, client_id: str | None = None, lang: str = "pl",
                 pause: float = 0.4, max_retries: int = 6):
        self.client_id = client_id or os.getenv("BDL_CLIENT_ID") or None
        self.lang = lang
        self.pause = pause
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers["Accept"] = "application/json"
        if self.client_id:
            self.session.headers["X-ClientId"] = self.client_id  # klucz nigdy do repozytorium

    def get(self, path: str, params: dict | None = None):
        url = f"{BASE_URL}/{path.lstrip('/')}"
        query = {"format": "json", "lang": self.lang, **(params or {})}
        for attempt in range(self.max_retries):
            resp = self.session.get(url, params=query, timeout=30)
            if resp.status_code == 429:  # limit zapytań
                wait = _retry_after_seconds(resp.headers.get("Retry-After"), attempt)
                print(f"429 - czekam {wait:.0f}s (próba {attempt + 1})")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            time.sleep(self.pause)
            return resp.json(), resp
        raise RuntimeError(f"Przekroczono limit ponowień dla {url}")

    def get_all_pages(self, path: str, params: dict | None = None,
                      page_size: int = 100, max_pages: int = 200) -> list[dict]:
        """Zwraca listę stron; odpowiedź API jest zapisana bez zmian w polu 'response'."""
        pages = []
        for page in range(max_pages):
            data, resp = self.get(path, {**(params or {}), "page": page, "page-size": page_size})
            pages.append({
                "request_url": resp.url,
                "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "rate_limit_headers": {k: v for k, v in resp.headers.items()
                                       if k.lower().startswith("x-rate")},
                "response": data,
            })
            results = data.get("results") or []
            total = data.get("totalRecords")
            if not results or (total is not None and (page + 1) * page_size >= total):
                break
        return pages
