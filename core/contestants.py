from typing import List, Optional
import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_ner():
    return pipeline(
        "ner",
        model="dslim/bert-base-NER",
        aggregation_strategy="simple"
    )
ALLOWED_LABELS = {"PERSON", "ORG", "GPE"}

BLOCK_TOKENS = {
    "vs", "v", "versus",
    "match", "highlights", "preview",
    "full", "final", "practice",
}

# Mapping HF → spaCy-style labels
LABEL_MAP = {
    "PER": "PERSON",
    "ORG": "ORG",
    "LOC": "GPE",
}


def extract_participants(normalized_query: str) -> Optional[List[str]]:
    ner = load_ner()
    entities = ner(normalized_query)

    seen = set()
    contestants = []

    for ent in entities:
        label = LABEL_MAP.get(ent["entity_group"])
        if label not in ALLOWED_LABELS:
            continue

        text = ent["word"]
        tokens = text.split()

        if any(tok in BLOCK_TOKENS for tok in tokens):
            continue

        if text not in seen:
            seen.add(text)
            contestants.append(text)

    return contestants if contestants else None
