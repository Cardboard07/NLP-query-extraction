# core/competition.py

from typing import Optional, List, Tuple
from pathlib import Path
import json
import numpy as np

from models.embedding import encode
from utils.similarity import cosine_similarity


# ----------------------------
# Load competitions registry
# ----------------------------

_COMPETITIONS_PATH = Path("data/competitions.json")

with open(_COMPETITIONS_PATH, "r") as f:
    _COMPETITIONS = {
        sport: [c.lower() for c in comps]
        for sport, comps in json.load(f).items()
    }


SEMANTIC_THRESHOLD = 0.35  # conservative by design


# ----------------------------
# Helpers
# ----------------------------

def _explicit_mentions(
    query_lc: str, allowed: List[str]
) -> List[str]:
    """
    Return competitions that are explicitly present
    as substrings in the query.
    """
    return [c for c in allowed if c in query_lc]


def _validate_semantically(
    sport: str,
    competition: str,
    query_vec: np.ndarray,
) -> float:
    """
    Return semantic similarity score for sport|competition pair.
    """
    pair_text = f"{sport} | {competition}"
    pair_vec = encode(pair_text)
    
    # FIX 1: Reshape 1D vectors -> 2D matrices (1 row, N columns)
    # FIX 2: Extract the scalar value ([0][0]) from the result matrix
    return cosine_similarity(
        query_vec.reshape(1, -1), 
        pair_vec.reshape(1, -1)
    )[0][0]


# ----------------------------
# Public API (LOCKED)
# ----------------------------

def detect_competition(
    query: str,
    sport: Optional[str],
    query_vec: np.ndarray,
) -> Optional[str]:
    """
    Extract and validate exactly one competition.
    """

    # HARD RULE: no sport → no competition
    if sport is None:
        return None

    sport = sport.lower()

    if sport not in _COMPETITIONS:
        return None

    allowed_competitions = _COMPETITIONS[sport]
    if not allowed_competitions:
        return None

    query_lc = query.lower()

    # STEP 1 — explicit mention check (NO INFERENCE)
    candidates = _explicit_mentions(query_lc, allowed_competitions)
    if not candidates:
        return None

    # STEP 2 — semantic validation
    valid: List[Tuple[str, float]] = []

    for comp in candidates:
        score = _validate_semantically(
            sport=sport,
            competition=comp,
            query_vec=query_vec,
        )

        if score >= SEMANTIC_THRESHOLD:
            valid.append((comp, score))

    if not valid:
        return None

    # STEP 3 — deterministic single output
    valid.sort(key=lambda x: x[1], reverse=True)
    return valid[0][0]
