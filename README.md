
python -V  # should be >= 3.10

# Create and activate venv
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the agentic pipeline
python src/run.py "Analyze ROAS drop in last 7 days"
# The project uses:
data/synthetic_fb_ads_undergarments.csv

# ⚙️ Config
config/config.yaml

project_name: "kasparro-agentic-fb-analyst"
random_seed: 42

# Minimum confidence to accept hypotheses
min_confidence: 0.6

data_csv: "data/synthetic_fb_ads_undergarments.csv"
date_col: "date"

# Gemini 2.0 Model
gemini:
  model: "gemini-2.0-flash"
  temperature: 0.0
  max_tokens: 800

report_dir: "reports"
logs_dir: "logs"
top_k_terms: 10


# Make sure to set your environment variable:
$env:GEMINI_API_KEY="YOUR_KEY"

# 📁 Repo Map

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

# ▶️ Run
python src/run.py "Analyze ROAS drop"

# 📤 Outputs

After running the pipeline, results are written to:

| File                     | Description                                 |
| ------------------------ | ------------------------------------------- |
| `reports/report.md`      | Executive summary for business stakeholders |
| `reports/insights.json`  | LLM-generated & validated hypotheses        |
| `reports/creatives.json` | Gemini-generated creative variants          |

# 👀 Observability

All agent steps write trace logs to:

logs/
  run.log
  insights.log
  creatives.log

[
  {
    "hypothesis_id": "H2",
    "campaign_id": "campaign_unknown",
    "variants": [
      {
        "variant_id": "v1",
        "headline": "Seamless Comfort, All Day Long",
        "body": "Discover bras and briefs designed for ultimate comfort and confidence. Free yourself from wires and embrace the feeling of seamless support. Shop our collection for women and men today!",
        "cta": "Shop Now",
        "reasoning": "Focuses on comfort and freedom from wires, addressing a potential pain point. Uses 'seamless' and 'comfort' prominently. Targets both women and men."
      },
      {
        "variant_id": "v2",
        "headline": "Confidence Starts From Within: Find Your Perfect Fit",
        "body": "Bras and briefs that empower you. Experience the difference of a perfectly fitting bra and comfortable briefs. Designed for women and men who value comfort and confidence, all day, every day.",
        "cta": "Find Your Fit",
        "reasoning": "Emphasizes confidence and finding the right fit. Uses 'confidence' and 'comfort' and targets both genders. The CTA encourages engagement beyond just shopping."
      },
      {
        "variant_id": "v3",
        "headline": "Free Yourself: Wire-Free Bras & Comfortable Briefs",
        "body": "Experience the ultimate in comfort with our wire-free bras and seamless briefs. Designed for women and men, our collection offers all-day support and confidence. Shop now and enjoy free shipping!",
        "cta": "Shop Free Shipping",
        "reasoning": "Highlights the 'free' aspect (wire-free and free shipping) and focuses on the benefits of wire-free bras and seamless briefs. Includes a shipping incentive. Targets both women and men."
      }
    ]
  }
]


# 🚀 Release
git tag v1.0
git push origin v1.0


📝 Self-Review (Design Choices & Tradeoffs)

This project implements a modular, agentic AI pipeline to analyze Facebook Ads performance using both statistical evaluation and LLM-driven reasoning. Below is a detailed self-review covering architecture, technical decisions, tradeoffs, reliability considerations, and opportunities for improvement.

1. Architecture & Design Decisions
✔ Multi-agent modular design

The system follows the required agentic workflow:

Planner — decomposes the user query into structured tasks

DataAgent — loads, validates, summarizes, and preprocesses the dataset

InsightAgent (Gemini 2.0 Flash) — generates hypotheses using dataset summary + planner tasks

Evaluator — validates each hypothesis using rule-based scoring and statistical signals

CreativeGenerator — generates creative variants using Gemini + TF-IDF keyword extraction

Reporter — compiles insights + creatives into clean, human-readable outputs

This separation improves maintainability, debugging, and extensibility.

2. LLM Model Selection: Gemini 2.0 Flash
Why Gemini 2.0 Flash?

Free, fast, and highly contextual

Better structured output reliability than older Gemini 1.x models

Supports generateContent, long context windows, and JSON-like outputs

Works within the constraints of free API usage

Tradeoff

Flash models are optimized for speed, not maximum creative reasoning

For real production, I would consider switching to Gemini 2.0 Pro for deeper insights

3. JSON Extraction & Robust Parsing

LLM responses are wrapped with a regex-based JSON extractor:

m = re.search(r"(\[.*\])", raw, flags=re.S)

Why this choice?

LLM outputs often include text before/after JSON.
Regex extraction provides more robustness vs. parsing raw text directly.

Tradeoff:

Regex can fail for malformed outputs → fallback is required.