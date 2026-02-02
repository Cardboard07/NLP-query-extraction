import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def best_match(query_vec, label_vecs, labels, threshold=0.4):
    scores = cosine_similarity([query_vec], label_vecs)[0]
    idx = int(np.argmax(scores))
    if scores[idx] < threshold:
        return None
    return labels[idx]
