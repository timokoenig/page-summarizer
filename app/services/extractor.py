import re
from urllib.parse import urlparse
import trafilatura

ALLOWED_SCHEMES = {"http", "https"}

def is_valid_url(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.scheme in ALLOWED_SCHEMES and bool(p.netloc)
    except Exception:
        return False

def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    text = re.sub(r"([\-=_]{3,}|[~]{3,})", " ", text)
    return text

def extract_main_content(url: str, favor_recall: bool = False) -> str:
    downloaded = trafilatura.fetch_url(url, no_ssl=False)
    if not downloaded:
        return ""
    extracted = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=False,
        favor_recall=favor_recall,
        with_metadata=False
    )
    return _clean_text(extracted or "")