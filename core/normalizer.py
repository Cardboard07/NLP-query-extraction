import re
from typing import Optional

# Optional: very small, deterministic typo map
# This is NOT ML, NOT fuzzy, NOT creative
# Only obvious, safe corrections
DEFAULT_TYPO_MAP = {
    "indai": "india",
    "inddia": "india",
    "ausstralia": "australia",
}


def normalize(
    query: str,
    spell_correct: bool = False,
    typo_map: Optional[dict] = None,
) -> str:
    """
    Convert a raw user query into a stable, comparable string
    without changing its meaning.
    """

    if not isinstance(query, str):
        raise TypeError("normalize() expects a string input")

    # 1️⃣ Lowercase
    text = query.lower()

    # 2️⃣ Normalize whitespace (tabs, newlines, multiple spaces)
    text = re.sub(r"\s+", " ", text).strip()

    # 3️⃣ Light punctuation cleanup
    # Keep: hyphens, numbers, slashes
    # Remove: commas, periods, excessive symbols
    text = re.sub(r"[.,!?:;\"'()\[\]{}]", "", text)

    # Remove leftover symbol noise (but keep - / and alphanumerics)
    text = re.sub(r"[^a-z0-9\-\/\s]", "", text)

    # Normalize whitespace again after removals
    text = re.sub(r"\s+", " ", text).strip()

    # 4️⃣ Optional deterministic spell correction
    if spell_correct:
        corrections = typo_map if typo_map is not None else DEFAULT_TYPO_MAP
        words = text.split(" ")
        words = [corrections.get(word, word) for word in words]
        text = " ".join(words)

    return text
