from typing import Optional, List
import re
from dateparser.search import search_dates


# ----------------------------
# Config / vocab
# ----------------------------

PREPOSITIONS = (
    "on ", "in ", "from ", "over ", "during ", 
    "the ", "of ", "for ", "at ", "since "
)

RELATIVE_PHRASES = [
    r"\btoday\b",
    r"\byesterday\b",
    r"\bthis year\b",
    r"\bthis month\b",
    r"\bnext week\b",
    r"\blast month\b",
    r"\blast year\b",
    r"\blast \d+ years\b",
]


# ----------------------------
# Helpers
# ----------------------------

def _is_invalid_match(text: str) -> bool:
    t = text.strip().lower()

    # Reject sports formats like T20
    if re.fullmatch(r"t\d+", t):
        return True

    # Reject very short junk (but keep valid years)
    if len(t) < 3 and not re.fullmatch(r"\d{4}", t):
        return True

    return False


def _strip_preposition(text: str) -> str:
    t = text.strip()
    for p in PREPOSITIONS:
        if t.lower().startswith(p):
            return t[len(p):].strip()
    return t


def _expand_duration(query: str, text: str) -> str:
    pattern = r"(last|past|previous)\s+" + re.escape(text)
    m = re.search(pattern, query.lower())
    return m.group(0) if m else text


def _remove_contained_dates(matches: List[str]) -> List[str]:
    """
    Remove less-specific dates contained in more-specific ones.
    Example: '2024' removed if 'December 2024' exists.
    """
    return [
        m for m in matches
        if not any(m != other and m in other for other in matches)
    ]


def _merge_ranges(query: str, matches: List[str]) -> Optional[str]:
    """
    Merge real ranges only (to / -), based on query order.
    """
    q = query.lower()

    ordered = sorted(matches, key=lambda x: q.find(x.lower()))

    for i in range(len(ordered) - 1):
        a, b = ordered[i], ordered[i + 1]
        pattern = re.escape(a.lower()) + r"\s*(to|-)\s*" + re.escape(b.lower())
        if re.search(pattern, q):
            return f"{a} to {b}"

    return None


# ----------------------------
# Main API
# ----------------------------

def extract_date(query: str) -> Optional[str]:
    if not query or not isinstance(query, str):
        return None

    # Step 1 — library extraction
    results = search_dates(
        query,
        settings={
            "RETURN_AS_TIMEZONE_AWARE": False,
            "STRICT_PARSING": False,
        },
    ) or []

    # Step 1.5 — manual year fallback (enumerations)
    manual_years = re.findall(r"\b((?:19|20)\d{2})\b", query)
    existing = {t for t, _ in results}
    for y in manual_years:
        if y not in existing:
            results.append((y, None))

    # Preserve query order
    results.sort(key=lambda x: query.find(x[0]))

    # Step 2 — clean candidates
    cleaned: List[str] = []
    for text, _ in results:
        t = _strip_preposition(text)
        t = " ".join(t.split())
        if _is_invalid_match(t):
            continue
        if t not in cleaned:
            cleaned.append(t)

    if not cleaned:
        # fallback relative phrases
        for pat in RELATIVE_PHRASES:
            m = re.search(pat, query.lower())
            if m:
                return m.group(0)
        return None

    # Step 3 — normalize meaning
    cleaned = [_expand_duration(query, t) for t in cleaned]
    cleaned = _remove_contained_dates(cleaned)

    # Step 4 — merge ranges
    merged = _merge_ranges(query, cleaned)
    if merged:
        return merged

    # Step 5 — choose most specific
    cleaned.sort(key=len, reverse=True)

    if cleaned and not re.fullmatch(r"\d{4}", cleaned[0]):
        return cleaned[0]

    # Step 6 — year fallback
    years = [t for t in cleaned if re.fullmatch(r"\d{4}", t)]
    if years:
        return years[0]

    return cleaned[0] if cleaned else None
