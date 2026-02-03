from sentence_transformers import SentenceTransformer
import numpy as np
import streamlit as st

_model = None

@st.cache_resource
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def encode(text: str) -> np.ndarray:
    model = get_model()
    return model.encode(text, normalize_embeddings=True)