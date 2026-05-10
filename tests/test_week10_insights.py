import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.analytics.pivot_builder import add_primary_category
from src.analytics.insight_reporter import run_all_questions

df = pd.read_csv("processed/cleaned/cleaned_data.csv")
df = df.rename(columns={"_id": "place_id"})
df = add_primary_category(df)

run_all_questions(df)