import pandas as pd
from pipeline import parse_query
from evaluate_predictions import run_slot_evaluation

queries = [
"Show me basketball highlights from yesterday", "Find MMA news regarding the next title fight", "What are the live football matches today?", "Show me upcoming soccer matches next week", "Find basketball analysis of the Lakers game", "Show me a preview of the UFC 300 card", "Find football highlights from last week", "Show me the 20th Dec soccer events", "Find India vs Pakistan match highlights from the 2023 World Cup", "List basketball matches scheduled for this weekend", "Show me MMA highlights from the latest Vegas event", "Find top 15 football highlights from November 2025", "Get me Madrid vs Sevilla match analysis", "Show me a preview for the upcoming NBA season", "Find news on the McGregor vs Chandler fight", "What are the Serie A matches for this week?", "Show me basketball news from the trade deadline", "Find MMA fight replays from last month", "Show me India vs Pakistan cricket news", "Find football matches involving Barcelona next week", "Show me basketball highlights for the last decade", "Find news on the England vs Australia cricket series", "Show me a tactical analysis of Liverpool's last game", "Find MMA matches scheduled for tomorrow night", "Show me a preview for the IPL 2026 season", "Find basketball highlights of all dunks this month", "Show me MMA news about the featherweight rankings", "Find football matches from the weekend", "Show me a preview of the next India vs Pakistan game", "Find basketball news regarding the Golden State Warriors", "Show me MMA analysis on the main event results", "Find football news from the French league", "Show me basketball highlights from the playoffs", "Find India vs Pakistan highlights from the 2019 World Cup", "Show me football highlights of the top saves this week", "Find MMA highlights of the best knockouts this year", "Show me a preview of the upcoming Asia Cup cricket", "Find basketball analysis for the Celtics vs Heat game", "Show me football news on player injuries this month", "Find MMA news regarding stadium events in London", "Show me cricket highlights of the highest ODI scores", "Find basketball matches from the last Olympic games", "Show me football matches from the Dutch league yesterday", "Find MMA analysis of the grappling exchanges last night", "Show me basketball news on the draft picks", "Find football news about the World Cup bidding process", "Show me cricket news on the domestic circuit", "Find MMA matches from the previous 48 hours", "Show me basketball match previews for the upcoming season", "Find football analysis for the Champions League semi-final", "Show me MMA news about the heavyweight champion", "Find cricket highlights from the 2022 T20 World Cup", "Show me basketball highlights from the EuroLeague", "Find football matches from the African Cup of Nations", "Show me MMA fight previews for the Saturday card", "Find basketball news about the All-Star game", "Show me football news regarding the national team coach", "Find India vs Pakistan match in 2007 T20 World Cup", "Show me MMA highlights from the PFL finals", "Find basketball analysis for the championship game", "Show me football news on the transfer window", "Find cricket news about the Ashes 2025", "Show me MMA news regarding the retirement of a legend", "Find basketball matches involving the Knicks today", "Show me football matches scheduled for next Christmas", "Find MMA highlights of the best submissions last week", "Show me a preview for the next Ashes test match", "Find basketball highlights of the rookie of the year", "Show me football analysis of the Manchester derby", "Find MMA news on the upcoming amateur tournament", "Show me cricket analysis of the spin bowling conditions", "Find basketball news from the Spanish league", "Show me football highlights from the FA Cup", "Find MMA highlights from the Bellator main event", "Show me basketball match previews for tonight", "Find football news regarding stadium renovations", "Show me cricket match highlights from last night's T20", "Find MMA analysis on the title contender's performance", "Show me basketball news on the injury report", "Find football highlights of the best free kicks this year", "Show me MMA match results from the Tokyo event", "Find basketball matches played in January 2024", "Show me football news for the Japanese league", "Find India vs Pakistan highlights from the 2003 World Cup", "Show me MMA news about the medical suspensions", "Find basketball highlights of the winning buzzer beater", "Show me football match previews for the upcoming qualifiers", "Find MMA highlights of the lightweight title defense", "Show me cricket news on the latest rankings", "Find basketball matches involving the Bucks next month", "Show me football analysis on the defensive performance last weekend", "Find MMA news on the press conference highlights", "Show me basketball highlights of the top blocks this season", "Find football matches from the Copa America", "Show me MMA previews for the next pay-per-view", "Find cricket news regarding the selection committee", "Show me basketball news from the college basketball tournament", "Find football highlights from the youth championship", "Show me MMA analysis on the scorecard controversy", "Find basketball matches scheduled for next Tuesday"
]

rows = []

for q in queries:
    result = parse_query(q)
    row = {"query": q}
    row.update(result)
    rows.append(row)

df = pd.DataFrame(rows)

# Pretty display (no truncation, no escapes)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", 200)

df
df_true = pd.read_excel("Sports Model Query Generation.xlsx")
df_pred = df

    # --- Sanity check ---
assert len(df_true) == len(df_pred), "Row count mismatch"

run_slot_evaluation(df_true=df_true, df_pred=df, categorical_slots=["entity.sport", "article_type"],fuzzy_slots=["entity.competition", "date"])

df.to_excel("my_data.xlsx", index=False)

