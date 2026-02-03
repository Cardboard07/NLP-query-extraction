import streamlit as st
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel


@st.cache_resource
def get_model():
    tokenizer = AutoTokenizer.from_pretrained(
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    model = AutoModel.from_pretrained(
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    model.eval()
    return tokenizer, model


def encode(text: str) -> np.ndarray:
    tokenizer, model = get_model()

    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)

    # Mean pooling (same idea as sentence-transformers)
    embeddings = outputs.last_hidden_state.mean(dim=1)

    # L2 normalize (equivalent to normalize_embeddings=True)
    embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

    return embeddings.cpu().numpy()
