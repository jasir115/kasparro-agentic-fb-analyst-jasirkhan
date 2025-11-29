<div align="center">

# 🚀 Kasparro — Agentic Facebook Ads Performance Analyst  
### AI-powered pipeline for marketing insights, diagnostics & creative generation  
**Built with Python · Gemini 2.0 Flash · Modular Agent Architecture**

---

</div>

## 🔥 Overview

Kasparro is a **production-style agentic system** that analyzes Facebook Ads performance end-to-end:

- 📌 Understands your question (ROAS drop, CTR dip, CPC spike, etc.)
- 📊 Summarizes & inspects the dataset
- 🧠 Generates data-backed hypotheses (via Gemini)
- 🧪 Validates them using statistical signals (rule-based evaluator)
- 🎨 Produces improved ad creatives (via Gemini + TF-IDF)
- 📝 Exports clean JSON + Markdown business reports

All components are modular and fully traceable.

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

▶️ Run the Full Pipeline
python src/run.py "Analyze ROAS drop in last 7 days"

📁 Project Structure
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
Config file: config/config.yaml
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

📤 Outputs
After running the pipeline, results appear in:

| File                     | Description                        |
| ------------------------ | ---------------------------------- |
| `reports/report.md`      | Executive summary for stakeholders |
| `reports/insights.json`  | Validated hypotheses               |
| `reports/creatives.json` | Generated creative ad variants     |

Example creative output:
{
  "headline": "Seamless Comfort, All Day Long",
  "cta": "Shop Now",
  "reasoning": "Highlights comfort & wire-free design."
}

👀 Observability
Full trace logs are automatically captured:
logs/
 ├── run.log
 ├── insights.log
 └── creatives.log

🚀 Release
git tag v1.0
git push origin v1.0
# 📝 Self-Review (Design Choices & Tradeoffs)

### ✔ Multi-agent modular architecture  
### ✔ Stable fallback systems (for LLM failures)  
### ✔ Gemini 2.0 Flash chosen for speed + structure  
### ✔ Regex-based JSON extraction  
### ✔ Rule-based evaluator for deterministic scoring  
### ✔ Observability-first design using logs  
### ✔ Robust creative generation using TF-IDF + LLM  

---

## 🔮 Limitations & Future Enhancements

- Add Pydantic for JSON schema validation  
- Enable multi-pass self-refinement of hypotheses  
- Add dashboards for ROAS/CTR visualization  
- Upgrade to Gemini 2.0 Pro for deeper insights  

---

<div align="center">

✨ **Built for Kasparro Assignment**  
📬 Need help running or improving this? Just ask!  

</div>
