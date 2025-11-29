<div align="center">

# 🚀 Kasparro — Agentic Facebook Ads Performance Analyst  
### AI-powered pipeline for marketing insights, diagnostics & creative generation  
**Built with Python · Gemini 2.0 Flash · Modular Agent Architecture**

---

</div>

## 🔥 Overview

Kasparro is a **production-style agentic system** that analyzes Facebook Ads performance end-to-end. It:

- 📌 Understands analytical queries (ROAS drop, CTR dip, CPC spike, etc.)
- 📊 Summarizes and inspects large ad datasets
- 🧠 Generates hypotheses using Gemini 2.0 Flash
- 🧪 Validates them using statistical heuristics (CTR/ROAS/CPC trends)
- 🎨 Generates improved ad creatives using TF-IDF + LLM
- 📝 Outputs clean JSON + Markdown business reports

All components are modular, traceable, and production-ready.

---

# 🛠 Quick Start

```bash
python -V  # should be >= 3.10

# Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the full pipeline
python src/run.py "Analyze ROAS drop in last 7 days"
📁 Project Structure
bash
Copy code
kasparro-agentic-fb-analyst/
│
├── README.md
├── requirements.txt
├── Makefile
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── synthetic_fb_ads_undergarments.csv
│   └── sample_fb_ads.csv
│
├── prompts/
│   ├── planner_prompt.md
│   ├── insight_prompt.md
│   ├── creative_prompt.md
│   └── eval_prompt.md
│
├── src/
│   ├── run.py
│   └── agents/
│       ├── planner.py
│       ├── data_agent.py
│       ├── insight_agent.py
│       ├── evaluator.py
│       └── creative_generator.py
│
├── reports/
│   ├── report.md
│   ├── insights.json
│   └── creatives.json
│
├── logs/
│   ├── run.log
│   ├── insights.log
│   └── creatives.log
│
└── tests/
    └── test_evaluator.py
⚙️ Configuration
yaml
Copy code
project_name: "kasparro-agentic-fb-analyst"
random_seed: 42
min_confidence: 0.6

data_csv: "data/synthetic_fb_ads_undergarments.csv"
date_col: "date"

gemini:
  model: "gemini-2.0-flash"
  temperature: 0.0
  max_tokens: 800

report_dir: "reports"
logs_dir: "logs"
top_k_terms: 10
Set your API key:

powershell
Copy code
$env:GEMINI_API_KEY="YOUR_KEY"
📤 Outputs
File	Description
reports/report.md	Executive summary for stakeholders
reports/insights.json	Validated hypotheses
reports/creatives.json	LLM-generated creative variants

Example output:

json
Copy code
{
  "headline": "Seamless Comfort, All Day Long",
  "cta": "Shop Now",
  "reasoning": "Highlights comfort & wire-free design."
}
👀 Observability
bash
Copy code
logs/
 ├── run.log
 ├── insights.log
 └── creatives.log
🚀 Release
bash
Copy code
git tag v1.0
git push origin v1.0
📝 Self-Review (Design Choices & Tradeoffs)
✔ Multi-agent modular architecture
✔ Stable fallback systems for LLM errors
✔ Gemini 2.0 Flash for speed + structured JSON
✔ Regex-backed JSON extraction for stability
✔ Rule-based evaluator for deterministic scoring
✔ Observability-first design using complete logging
✔ TF-IDF + LLM creative generation

🔮 Limitations & Future Enhancements
Add Pydantic for JSON schema validation

Enable multi-pass self-refinement of hypotheses

Add dashboards for ROAS/CTR visualization

Upgrade to Gemini 2.0 Pro for deeper insights

<div align="center">
✨ Built for Kasparro Assignment
📬 Need help running or improving this? Just ask!

</div> ```
