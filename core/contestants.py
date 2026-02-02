import spacy
from typing import List, Optional

nlp = spacy.load("en_core_web_sm")

ALLOWED_LABELS = {"PERSON", "ORG", "GPE"}

BLOCK_TOKENS = {
    "vs", "v", "versus",
    "match", "highlights", "preview",
    "full", "final", "practice",
}

def extract_participants(normalized_query: str) -> Optional[List[str]]:
    doc = nlp(normalized_query)

    seen = set()
    contestants = []

    for ent in doc.ents:
        if ent.label_ not in ALLOWED_LABELS:
            continue

        tokens = ent.text.split()
        if any(tok in BLOCK_TOKENS for tok in tokens):
            continue

        if ent.text not in seen:
            seen.add(ent.text)
            contestants.append(ent.text)

    return contestants if contestants else None
