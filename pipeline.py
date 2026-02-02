from core.normalizer import normalize
from models.embedding import encode
from core.sport import detect_sport
from core.competition import detect_competition
from core.contestants import extract_participants
from core.article_type import detect_article_type
from core.date import extract_date


def parse_query(query: str) -> dict:
    """
    Main query understanding pipeline.
    Takes a raw query string and returns a structured JSON-like dict.
    """

    # --- Step 0: normalization ---
    normalized_query = normalize(query)

    # --- Step 1: embedding (ONCE) ---
    query_vec = encode(normalized_query)

    # --- Step 2: sport detection ---
    sport = detect_sport(query_vec)

    # --- Step 3: competition detection (sport-gated internally) ---
    competition = detect_competition(
        normalized_query,
        sport,
        query_vec
    )

    # --- Step 4: contestants ---
    contestants = extract_participants(normalized_query)

    # --- Step 5: article type ---
    article_type = detect_article_type(normalized_query)

    # --- Step 6: date ---
    date = extract_date(normalized_query)

    # --- Final structured output ---
    return {
        "entity.sport": sport,
        "entity.competition": competition,
        "entity.contestants": contestants,
        "article_type": article_type,
        "date": date
    }
