from core.date import extract_date

queries = [
    # absolute dates
    "India T20 matches December 2025",
    "Ashes 2023 highlights",
    "matches on 12 December 2024",
    "March 14 boxing fight",

    # relative dates
    "UFC fights next week",
    "football matches last month",
    "cricket news this year",
    "boxing bout yesterday",

    # ranges / seasons
    "India matches in 2024-25 season",
    "matches from December 2024 to January 2025",
    "performance over last 3 years",

    # implicit / partial
    "December matches",
    "matches in 2025",
    "matches in summer",

    # multiple dates (must pick ONE)
    "India matches in 2023 and 2024",
    "boxing fights from 2021 to 2023",

    # negatives
    "India T20 matches",
    "highlights of the final",
    "sports news today",
    "",
]

print("=" * 60)
for q in queries:
    result = extract_date(q)
    print(f"Query   : {q}")
    print(f"Extract : {result}")
    print("-" * 60)
