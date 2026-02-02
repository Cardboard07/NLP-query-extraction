import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
from difflib import SequenceMatcher

def run_slot_evaluation(df_true, df_pred, categorical_slots=None, fuzzy_slots=None, fuzzy_threshold=0.8):
    """
    Comprehensive evaluator for slot-filling tasks.
    
    Args:
        df_true: Ground truth DataFrame
        df_pred: Model predictions DataFrame
        categorical_slots: List of columns for exact/F1 metrics (e.g., ['article_type'])
        fuzzy_slots: List of columns for similarity scoring (e.g., ['entity.competition'])
    """
    
    def normalize(s):
        return s.fillna("none").astype(str).str.strip().str.lower()

    def get_fuzzy_ratio(a, b):
        return SequenceMatcher(None, a, b).ratio()

    # --- 1. Categorical Slots (Exact Match + F1) ---
    if categorical_slots:
        for col in categorical_slots:
            y_true = normalize(df_true[col])
            y_pred = normalize(df_pred[col])
            
            coverage = (y_pred != "none").mean()
            
            print(f"\n{'='*20} CATEGORICAL: {col} {'='*20}")
            print(f"Coverage: {coverage:.2%}")
            print(classification_report(y_true, y_pred, zero_division=0))

    # --- 2. Fuzzy Slots (Similarity Scoring) ---
    if fuzzy_slots:
        for col in fuzzy_slots:
            y_true = normalize(df_true[col])
            y_pred = normalize(df_pred[col])
            
            # Calculate fuzzy scores for each row
            scores = [get_fuzzy_ratio(t, p) for t, p in zip(y_true, y_pred)]
            avg_fuzzy = sum(scores) / len(scores)
            
            print(f"\n{'='*20} FUZZY: {col} {'='*20}")
            print(f"Average Similarity Score: {avg_fuzzy:.2%}")
            
            # Print samples of "near misses" (errors that were close)
            print("\nSample Analysis (Top Errors):")
            error_count = 0
            for i, (t, p, s) in enumerate(zip(y_true, y_pred, scores)):
                if t != p and error_count < 5:
                    status = "⚠️ Close" if s >= fuzzy_threshold else "❌ Miss"
                    print(f"Row {i} | Truth: {t:<15} | Pred: {p:<15} | [{status} - Score: {s:.2f}]")
                    error_count += 1

# --- Example Usage ---
# run_slot_evaluation(
#     df_true=test_df, 
#     df_pred=pred_df, 
#     categorical_slots=["entity.sport", "article_type"],
#     fuzzy_slots=["entity.competition", "date"]
# )