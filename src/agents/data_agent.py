import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer

class DataAgent:
    def __init__(self, cfg):
        self.cfg = cfg

    def load(self, path=None):
        path = path or self.cfg["data_csv"]
        df = pd.read_csv(path, parse_dates=[self.cfg.get("date_col","date")])
        # coerce common numeric fields if present
        for c in ["spend","impressions","clicks","conversions","roas","ctr","cpc"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
        self.df = df
        return df

    def basic_summary(self):
        df = self.df
        summary = {
            "rows": int(len(df)),
            "cols": list(df.columns),
            "date_range": [str(df[self.cfg.get("date_col","date")].min()), str(df[self.cfg.get("date_col","date")].max())],
        }
        if "spend" in df:
            summary["total_spend"] = float(df["spend"].sum(skipna=True))
        if "impressions" in df:
            summary["total_impressions"] = int(df["impressions"].sum(skipna=True))
        if "ctr" in df:
            summary["avg_ctr"] = float(df["ctr"].mean(skipna=True))
        if "roas" in df:
            summary["avg_roas"] = float(df["roas"].mean(skipna=True))
        return summary

    def top_terms_from_creatives(self, n=10, text_col="creative_text"):
        df = self.df
        if text_col not in df.columns:
            return []
        texts = df[text_col].fillna("").astype(str).values
        if not any(texts):
            return []
        vec = TfidfVectorizer(max_features=500, stop_words="english", ngram_range=(1,2))
        X = vec.fit_transform(texts)
        tfidf_sum = X.sum(axis=0).A1
        terms = [(t, tfidf_sum[i]) for i,t in enumerate(vec.get_feature_names_out())]
        terms = sorted(terms, key=lambda x: -x[1])
        return [t for t,_ in terms[:n]]
