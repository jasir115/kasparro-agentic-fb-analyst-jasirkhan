import os

import json
import google.generativeai as genai
from .data_agent import DataAgent

class CreativeGenerator:
    def __init__(self, cfg):
        self.cfg = cfg
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            print("⚠️ GEMINI_API_KEY not set. LLM calls disabled.")
            self.model = None
            return

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.cfg["gemini"]["model"])

    def _call_llm(self, prompt):
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": float(self.cfg["gemini"].get("temperature", 0.7)),
                "max_output_tokens": int(self.cfg["gemini"].get("max_tokens", 800)),
            }
        )
        return response.text

    def generate_creatives(self, hypotheses, df):
        creatives = []

        da = DataAgent(self.cfg)
        df_loaded = da.load(self.cfg["data_csv"])
        top_terms = da.top_terms_from_creatives(
            n=self.cfg.get("top_k_terms", 10),
            text_col="creative_message"
        )

        for h in hypotheses:
            if "creative" in h["text"].lower() or "ctr" in h["text"].lower():
                campaign_id = h.get("campaign_id", "campaign_unknown")

                prompt = f"""
Create 3 Facebook ad variants based on:
Hypothesis: {h['text']}
Top terms: {top_terms}

Return only valid JSON array:
[
  {{
    "variant_id": "v1",
    "headline": "...",
    "body": "...",
    "cta": "...",
    "reasoning": "..."
  }}
]
"""

                try:
                    raw = self._call_llm(prompt)
                    import re
                    m = re.search(r"(\[.*\])", raw, flags=re.S)
                    if m:
                        arr = json.loads(m.group(1))
                    else:
                        arr = json.loads(raw)

                except Exception:
                    arr = []
                    for i in range(3):
                        term = top_terms[i % len(top_terms)] if top_terms else "Comfort"
                        arr.append({
                            "variant_id": f"{campaign_id}_v{i+1}",
                            "headline": f"{term.title()} — Comfort You Can Feel",
                            "body": f"Try our {term} undergarments for all-day comfort.",
                            "cta": "Shop Now",
                            "reasoning": "Fallback variant using top terms"
                        })

                creatives.append({
                    "hypothesis_id": h["id"],
                    "campaign_id": campaign_id,
                    "variants": arr
                })

        return creatives
