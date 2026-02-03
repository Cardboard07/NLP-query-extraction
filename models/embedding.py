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
        return_tensors="pt",
        truncation=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    embedding = outputs.last_hidden_state.mean(dim=1)
    embedding = torch.nn.functional.normalize(embedding, p=2, dim=1)

    return embedding.cpu().numpy()[0]  # <- FIX

