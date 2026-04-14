import json
import os
import pandas as pd

# ---------------------------------------------------------
# Task 2: Clean CSV
# ---------------------------------------------------------
def task2_clean_data(json_filename):
    print("\n--- Task 2: Clean the Data ---")
    if not json_filename or not os.path.exists(json_filename):
        print("JSON file not found. Skipping Task 2.")
        return None
        
    df = pd.read_json(json_filename)
    print(f"Loaded {len(df)} stories from {json_filename}")
    
    # 1. Duplicates
    df = df.drop_duplicates(subset=["post_id"])
    print(f"After removing duplicates: {len(df)}")
    
    # 2. Missing values
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")
    
    # Fill missing num_comments with 0 so we can convert to integer
    df["num_comments"] = df["num_comments"].fillna(0)
    
    # 3. Data types
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)
    
    # 4. Low quality
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")
    
    # 5. Whitespace
    df["title"] = df["title"].str.strip()
    
    out_csv = "data/trends_clean.csv"
    df.to_csv(out_csv, index=False)
    print(f"\nSaved {len(df)} rows to {out_csv}\n")
    
    print("Stories per category:")
    counts = df["category"].value_counts()
    for cat, count in counts.items():
        print(f"  {cat.ljust(15)} {count}")
    
    return out_csv