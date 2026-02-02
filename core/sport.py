import json
from pathlib import Path
from typing import Optional

import numpy as np

# ---- Configuration ----
SIMILARITY_THRESHOLD =  0.35  # or even 0.55


# ---- Load sport labels ----
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sports.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    SPORT_LABELS = json.load(f)

# ---- Import encoder (must already normalize vectors) ----
from models.embedding import encode
  # adjust import if needed

# ---- Precompute sport label embeddings (ONCE) ----
SPORT_EMBEDDINGS = {}

for sport, phrases in SPORT_LABELS.items():
    vecs = [encode(p) for p in phrases]
    SPORT_EMBEDDINGS[sport] = np.mean(vecs, axis=0)



def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Assumes a and b are already L2-normalized.
    """
    return float(np.dot(a, b))


def detect_sport(query_vec: np.ndarray) -> Optional[str]:
    """
    Infer the sport implied by a query embedding using semantic similarity.
    Returns a canonical sport string or None.
    """

    best_sport = None
    best_score = -1.0

    for sport, sport_vec in SPORT_EMBEDDINGS.items():
        score = cosine_similarity(query_vec, sport_vec)

        if score > best_score:
            best_score = score
            best_sport = sport

    if best_score < SIMILARITY_THRESHOLD:
        return None

    return best_sport
