<div align="center">

# 🚀 Kasparro — Agentic Facebook Ads Performance Analyst  
### AI-powered pipeline for marketing insights, diagnostics & creative generation  
**Built with Python · Gemini 2.0 Flash · Modular Agent Architecture**

---

</div>

## 🔥 Overview
Kasparro is a production-style agentic system that analyzes Facebook Ads performance end-to-end. It understands analytical queries (ROAS drop, CTR dip, CPC spike), summarizes and inspects your dataset, generates hypotheses via Gemini 2.0 Flash, validates them using rule-based statistical evaluation, generates improved ad creatives using TF-IDF + LLM, and exports insights and creatives as clean JSON + Markdown reports. Every component is modular, traceable, and production-ready.

## 🛠 Quick Start
python -V  # should be >= 3.10  
python -m venv .venv  
.venv\Scripts\activate    # Windows  
pip install -r requirements.txt  
python src/run.py "Analyze ROAS drop in last 7 days"

## 📁 Project Structure
kasparro-agentic-fb-analyst/  
├── README.md  
├── requirements.txt  
├── Makefile  
├── config/config.yaml  
├── data/synthetic_fb_ads_undergarments.csv  
├── prompts/*.md  
├── src/run.py  
├── src/agents/ (planner, data_agent, insight_agent, evaluator, creative_generator)  
├── reports/ (report.md, insights.json, creatives.json)  
├── logs/ (run.log, insights.log, creatives.log)  
└── tests/test_evaluator.py  

## ⚙️ Config (config/config.yaml)
project_name: kasparro-agentic-fb-analyst  
random_seed: 42  
min_confidence: 0.6  
data_csv: data/synthetic_fb_ads_undergarments.csv  
date_col: date  
gemini_model: gemini-2.0-flash  
temperature: 0.0  
max_tokens: 800  
report_dir: reports  
logs_dir: logs  
top_k_terms: 10  

Set API key:  
$env:GEMINI_API_KEY="YOUR_KEY"

## 📤 Outputs
reports/report.md — Executive summary  
reports/insights.json — Validated hypotheses  
reports/creatives.json — Creative variants  

Example creative output (displayed as plain text here):  
headline: Seamless Comfort, All Day Long  
cta: Shop Now  
reasoning: Highlights comfort & wire-free design.  

## 👀 Observability
logs/run.log  
logs/insights.log  
logs/creatives.log  

## 🚀 Release
git tag v1.0  
git push origin v1.0

## 📝 Self-Review (Design Choices & Tradeoffs)
✔ Multi-agent modular architecture  
✔ Stable fallback systems for LLM errors  
✔ Gemini 2.0 Flash for speed + structured output  
✔ Regex-backed JSON extraction  
✔ Rule-based deterministic evaluator  
✔ Complete logging for observability  
✔ Creative generation using TF-IDF + LLM  

## 🔮 Limitations & Future Enhancements
- Add Pydantic schema validation  
- Add dashboards for ROAS and CTR visualization  
- Multi-pass reasoning for better hypothesis refinement  
- Upgrade to Gemini 2.0 Pro for deeper insight quality  

<div align="center">

✨ Built for Kasparro Assignment  
📬 Need help running or improving this? Just ask!  

</div>
