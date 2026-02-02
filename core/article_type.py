# core/article_type.py

from typing import Optional
import re

# Closed set of canonical article types
# Priority order: first match wins
ARTICLE_TYPES_PRIORITY = [
    "highlights",
    "matches",
    "analysis",
    "preview",
    "news",
]


def detect_article_type(query: str) -> Optional[str]:
    """
    Detects the article type explicitly mentioned in the query using
    deterministic whole-word matching.

    Args:
        query (str): Normalized query string (already lowercased).

    Returns:
        Optional[str]: Canonical article type if found, else None.
    """
    if not query:
        return None

    for article_type in ARTICLE_TYPES_PRIORITY:
        # Whole-word match only (no substrings)
        pattern = rf"\b{re.escape(article_type)}\b"
        if re.search(pattern, query):
            return article_type

    return None
