import os, json, time
import google.generativeai as genai

from .data_agent import DataAgent

class InsightAgent:
    def __init__(self, cfg):
        self.cfg = cfg
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ GEMINI_API_KEY not set. LLM calls disabled.")
            self.client = None
            return

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.cfg["gemini"]["model"])

    def _call_llm(self, prompt):
        if not self.model:
            raise RuntimeError("Gemini client not initialized")

        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": float(self.cfg["gemini"].get("temperature", 0.0)),
                "max_output_tokens": int(self.cfg["gemini"].get("max_tokens", 800)),
            }
        )
        return response.text

    def propose_hypotheses(self, query, summary, df, tasks):
        prompt = f"""
You are a senior marketing data analyst.

User query: {query}

Dataset summary:
{json.dumps(summary, indent=2)}

Columns: {summary.get('cols', [])}

Task plan: {tasks}

Generate 3–4 hypotheses explaining performance changes.
Return only a JSON array with this schema:
[
  {{
    "id": "H1",
    "text": "...",
    "confidence": 0.0,
    "suggested_checks": ["ctr_by_creative", ...]
  }}
]
"""

        try:
            raw = self._call_llm(prompt)
            import re
            m = re.search(r"(\[.*\])", raw, flags=re.S)
            if m:
                return json.loads(m.group(1))
            return json.loads(raw)
        except Exception as e:
            print("⚠️ Gemini JSON parse failed. Using fallback.", e)
            return self._fallback_hypotheses(summary, df)

    def _fallback_hypotheses(self, summary, df):
        hyps = []

        if "roas" in df.columns:
            hyps.append({
                "id": "H1",
                "text": "ROAS decreased — may be caused by weaker conversion rate or targeting shifts.",
                "confidence": 0.6,
                "suggested_checks": ["compare_roas_by_campaign", "compare_ctr"]
            })

        if "ctr" in df.columns:
            hyps.append({
                "id": "H2",
                "text": "CTR decreased — creatives may be suffering from fatigue or weak messaging.",
                "confidence": 0.65,
                "suggested_checks": ["ctr_by_creative", "ctr_by_audience"]
            })

        hyps.append({
            "id": "H3",
            "text": "Conversion rate drop — consider landing page or tracking issues.",
            "confidence": 0.5,
            "suggested_checks": ["conversion_rate_by_campaign"]
        })

        return hyps
