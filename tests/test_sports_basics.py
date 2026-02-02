from core.normalizer import normalize
from models.embedding import encode
from core.sport import detect_sport

def test_cricket_queries():
    q = "India T20 matches"
    vec = encode(normalize(q))
    assert detect_sport(vec) == "cricket"

def test_mma_queries():
    q = "UFC fight night"
    vec = encode(normalize(q))
    assert detect_sport(vec) == "mma"

def test_unknown_queries():
    q = "general sports news"
    vec = encode(normalize(q))
    assert detect_sport(vec) is None

