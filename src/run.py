import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import yaml
import json
from pathlib import Path
from src.agents.data_agent import DataAgent
from src.agents.planner import Planner
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator import Evaluator
from src.agents.creative_generator import CreativeGenerator

def ensure_dirs(cfg):
    Path(cfg["report_dir"]).mkdir(parents=True, exist_ok=True)
    Path(cfg["logs_dir"]).mkdir(parents=True, exist_ok=True)

def main():
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Analysis query string", nargs="?")
    args = parser.parse_args()
    query = args.query or "Analyze ROAS drop"

    cfg = yaml.safe_load(open("config/config.yaml"))
    ensure_dirs(cfg)

    # Data
    data_agent = DataAgent(cfg)
    df = data_agent.load(cfg["data_csv"])
    summary = data_agent.basic_summary()

    # Planner
    planner = Planner(cfg)
    tasks = planner.plan(query, summary)

    # Insights (LLM)
    insight_agent = InsightAgent(cfg)
    hypotheses = insight_agent.propose_hypotheses(query, summary, df, tasks)

    # Evaluator
    evaluator = Evaluator(cfg)
    validated = evaluator.validate_hypotheses(hypotheses, df)

    # Creative generation
    creative_gen = CreativeGenerator(cfg)
    creatives = creative_gen.generate_creatives(validated, df)

    # Save outputs
    Path(cfg["report_dir"]).joinpath("insights.json").write_text(json.dumps(validated, indent=2))
    Path(cfg["report_dir"]).joinpath("creatives.json").write_text(json.dumps(creatives, indent=2))

    # Basic report.md
    report_md = Path(cfg["report_dir"]).joinpath("report.md")
    report_md.write_text("# Analysis Report\n\n" +
                         f"Query: {query}\n\n" +
                         "## Top hypotheses\n\n" +
                         "\n".join([f"- {h['id']}: {h['text']} (confidence: {h.get('confidence', 'n/a')})" for h in validated]))
    print("Done. Reports written to", cfg["report_dir"])

if __name__ == "__main__":
    main()
