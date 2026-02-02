from core.normalizer import normalize
from models.embedding import encode
from core.sport import detect_sport
from core.competition import detect_competition

def test_valid_competition():
    q = "India T20 matches"
    vec = encode(normalize(q))
    sport = detect_sport(vec)

    assert detect_competition(normalize(q), sport, vec) == "T20"

def test_cross_sport_rejection():
    q = "T20 boxing match"
    vec = encode(normalize(q))
    sport = detect_sport(vec)

    assert detect_competition(normalize(q), sport, vec) is None

def test_missing_competition():
    q = "India cricket matches"
    vec = encode(normalize(q))
    sport = detect_sport(vec)

    assert detect_competition(normalize(q), sport, vec) is None
